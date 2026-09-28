from pydantic import BaseModel
from tools.Tool import Tool
from tools.ToolRegistry import ToolRegistry
from datetime import datetime
from utils.utils import load_data

import os
import json

_SRE_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sre_data.json")

class CheckDeploymentsArgs(BaseModel):
     app_id: int
class GetRunBookArgs(BaseModel):
     query: str
class SendMessageArgs(BaseModel):
     message: str
class ReadLogsArgs(BaseModel):
     app_id: int
     timestamp: str

class Sre:
     def getRunBook(query:str):
          runbook = load_data(_SRE_DATA_PATH)["runbook"]
          terms = [w for w in query.lower().split() if len(w) > 3]
          scored = []
          for entry in runbook:
               text = entry["description"].lower()
               score = sum(1 for t in terms if t in text)
               if score:
                    scored.append((score, entry))
          scored.sort(key=lambda pair: pair[0], reverse=True)
          return [entry for _, entry in scored[:2]]
     
     def checkDeployments(app_id:int):
          return load_data(_SRE_DATA_PATH)["deployments"].get(str(app_id), [])
     
     def sendMessage(message:str):
          print("Message to Humans:",message)

     def readLogs(app_id:int, timestamp:str):
          lst={int(k): v for k, v in load_data(_SRE_DATA_PATH)["logs"].items()}
          lst[app_id].sort(key=lambda entry:entry["timestamp"])
          for i, item in enumerate(lst[app_id]):
               if datetime.strptime(item["timestamp"],"%Y-%m-%d %H:%M:%S") < datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"):
                    continue
               else:
                    if datetime.strptime(item["timestamp"],"%Y-%m-%d %H:%M:%S") == datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"):
                         return item["log"]
                    break
          if i-1>=0: 
               return lst[app_id][i-1]["log"]
          return lst[app_id][i]["log"]

     class SreTools:
          def __init__(self):
               self.checkDeploymentsTool:Tool=Tool(
                    name="checkDeployments",
                    description="this tool is to check deployment details for an application using application id calling this tool with application id will give snapshot of health of each deployed component for that respective application. use this tool to know about deployment for an app using its id",
                    args_schema=CheckDeploymentsArgs,
                    isReadOnly=True,
                    func=Sre.checkDeployments
                    )
               self.getRunBookTool:Tool=Tool(
                    name="getRunbook",
                    description="Searches the runbook (a record of known incidents and their remediation) and returns only the entries matching your query. Pass a short query of the key symptom or root-cause keywords you saw in the logs or metrics (e.g. 'connection pool exhausted', 'memory leak after deploy', 'cache stampede', 'disk pressure'). Returns up to 2 best-matching entries, or an empty list if nothing matches (broaden or change your keywords). The runbook does not cover every possible issue.",
                    args_schema=GetRunBookArgs,
                    isReadOnly=True,
                    func=Sre.getRunBook
               )
               self.sendMessageTool:Tool=Tool(
                    name="sendMessage",
                    description="Delivers your ONE final triage to humans (problem, root cause, recommended fix). Use it EXACTLY ONCE, only when your investigation is complete and you are confident. Do NOT use it for progress updates, partial findings, intermediate summaries, or to ask questions. Immediately after calling it, call stop in the same turn. If you are not yet ready to deliver the final triage, do not call this - keep investigating instead.",
                    args_schema=SendMessageArgs,
                    isReadOnly=False,
                    func=Sre.sendMessage
               )
               self.readLogsTool:Tool=Tool(
                    name="readLogs",
                    description='Reads what actually happened in a service at a point in time. ALWAYS read the relevant logs here before concluding a root cause - do not conclude from deployment metrics alone, the logs are the source of truth. Provide the service id (app_id) and a timestamp; it returns the log entry at that exact timestamp, or the nearest one immediately before it if that exact timestamp has no entry. It returns ONE entry per call, so step forward through time (start from the deployment unhealthy_since and advance) to follow the incident. Timestamp format must be "%Y-%m-%d %H:%M:%S".',
                    args_schema=ReadLogsArgs,
                    isReadOnly=True,
                    func=Sre.readLogs
               )
          def _allTools(self):
               return [
                    self.checkDeploymentsTool,
                    self.getRunBookTool,
                    self.sendMessageTool,
                    self.readLogsTool
               ]

          def toRegistry(self):
               registry = ToolRegistry()
               for tool in self._allTools():
                    registry.register(tool)
               return registry

registry=Sre.SreTools().toRegistry()