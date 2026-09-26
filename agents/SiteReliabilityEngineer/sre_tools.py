from pydantic import BaseModel
from tools.Tool import Tool
from datetime import datetime


class CheckDeploymentsArgs(BaseModel):
     app_id: int


class GetRunBookArgs(BaseModel):
     pass


class SendMessageArgs(BaseModel):
     message: str


class ReadLogsArgs(BaseModel):
     app_id: int
     timestamp: str


class StopArgs(BaseModel):
     pass


class Sre:
     def getRunBook():
          return[
               {
                    "description":"when any instance of a service is down",
                    "resolution":"then scale the service to zeero then scale service to original number of instances this brings all instances up"
               }
          ]
     def checkDeployments(app_id:int):
          return[
               {
                    "id":1,
                    "instances":5,
                    "down":0,
                    "qps":15000,
                    "qpsthreshold":12000,
                    "fps":300,
                    "fpsthreshold":200
               }
          ]
     def sendMessage(message:str):
          print("Message to Humans:",message)

     def readLogs(app_id:int, timestamp:str):
          lst={
               1:[
                    {
                         "timestamp":"2026-09-25 12:00:00",
                         "log":"system fetch user details and failed error happened connection pool exhausted"
                    },
                    {
                         "timestamp":"2026-09-25 12:00:10",
                         "log":"system retried and fetch user details successfully"
                    },
                    {
                         "timestamp":"2026-09-25 12:00:20",
                         "log":"performed business logic, could not write to database"
                    },
                    {
                         "timestamp":"2026-09-25 12:00:30",
                         "log":"performing retry to write into databse"
                    },
                    {
                         "timestamp":"2026-09-25 12:00:40",
                         "log":"write to database failed"
                    },
                    {
                         "timestamp":"2026-09-25 12:00:50",
                         "log":"too many requests exiting"
                    }
               ]
          }
          lst[app_id].sort(key=lambda entry:entry["timestamp"])
          for i, item in enumerate(lst[app_id]):
               if datetime.strptime(item["timestamp"],"%Y-%m-%d %H:%M:%S") < datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"):
                    continue
               else:
                    if datetime.strptime(item["timestamp"],"%Y-%m-%d %H:%M:%S") == datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"):
                         return item["timestamp"]
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
                    func=Sre.checkDeployments
                    )
               self.getRunBookTool:Tool=Tool(
                    name="getRunbook",
                    description="this function gets the runbook for issues resolution. runbook  basically is a record of known incidents and what needs to be done when such issues occur. following runbook steps for exact same issue resolves the issue, remember runbook does not give you answer to all possible issue it is only list of known issues for which remediation is recorded",
                    args_schema=GetRunBookArgs,
                    func=Sre.getRunBook
               )
               self.sendMessageTool:Tool=Tool(
                    name="sendMessage",
                    description="this tool is to send message over human teams channel this tool is importatnt to let human know something. use this tool to send final triage information, do not use this tool to seek help from human, do not use this just to know something intermediary",
                    args_schema=SendMessageArgs,
                    func=Sre.sendMessage
               )
               self.readLogsTool:Tool=Tool(
                    name="readLogs",
                    description='use this tool when you are not sure what happened or have no clue why this incident was raised, to read logs based on timestamp you provided for service whose service id you provide, these logs would help you know what actually happened in the service at a point in time, you can provide single timestamp which will fetch you lines for that exact timestamp, or if the exact timestamp entry does not exsist then it will give you an entries which is immediately before provided timestamp.remember you can only fethc logs one entry at a time, timestamp should be in format "%Y-%m-%d %H:%M:%S"',
                    args_schema=ReadLogsArgs,
                    func=Sre.readLogs
               )
               self.stop:Tool = Tool(
                    name="stop",
                    description="this tool is to indicate that the work is done, know that this tool is to be called only and only when you have finished the job and have achieved the goal specified",
                    args_schema=StopArgs,
                    func=None
               )
          def _allTools(self):
               return [
                    self.checkDeploymentsTool,
                    self.getRunBookTool,
                    self.sendMessageTool,
                    self.readLogsTool,
                    self.stop,
               ]

          def getToolsForLiteLlm(self):
               return [{"type": "function", "function": tool.schema()} for tool in self._allTools()]

          def getToolMap(self):
               return {tool.name: tool for tool in self._allTools()}

_sreTools=Sre.SreTools()
tools=_sreTools.getToolsForLiteLlm()
tool_map=_sreTools.getToolMap()