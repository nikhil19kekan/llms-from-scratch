from core.llm import Llm
import queue
import json
from agents.SiteReliabilityEngineer.incident import Incident
from agents.SiteReliabilityEngineer.sre_tools import tools, tool_map
class SreAgent:
     roundtrips=None
     system_prompt=None
     llm:Llm=None
     queue=None
     
     def __init__(self):
          self.roundtrips=10
          self.system_prompt=f"you are a site reliability engineer, use tools given to you think which tool to use for what you have only {self.roundtrips} iterations in loop avaialble to reach goal of traiging the incident. be short and precise. logs is source of truth insterad of shooting in the dark"
          self.llm=Llm(system=self.system_prompt, tools=tools)
          self.queue=queue.Queue(maxsize=10)
     def queueIncident(self,inc:Incident):
          self.queue.put_nowait(inc)
     def receiveIncident(self):
          return self.queue.get_nowait()
     def triage(self):
          inc:Incident = self.receiveIncident()
          self.llm.add_user(
               f"achieve your goal for this incident. "
               f"app_id: {inc.app_id}, deployment_id: {inc.deployment_id}, issue: {inc.description}"
          )
          done=False
          for _ in range(self.roundtrips):
               response=self.llm.ask()
               print("MODELS THOUGHT:", response.content)
               self.llm.add_message(response)
               # if not response.tool_calls:
               #      print("FINAL ANSWER:", response.content)
               #      break
               # done=False
               for call in response.tool_calls:
                    if call.function.name == "stop":
                         done=True
                         break
                    tool=tool_map[call.function.name]
                    args=json.loads(call.function.arguments)
                    result=tool.run(**args)
                    print(f"RAN TOOL:{call.function.name} ARGUMENTS:({args}) RESULT: {result}")
                    self.llm.add_tool_result(call.id, json.dumps(result))
               if done:
                    print("model called stop")
                    break


