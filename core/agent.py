from core.llm import Llm
import queue
import json
class Agent:
     max_tokens=None
     system_prompt=None
     llm:Llm=None
     task_queue=None
     registry=None

     def __init__(self, maxTokens, systemPrompt, registry):
          self.max_tokens=maxTokens
          self.system_prompt=systemPrompt
          self.registry=registry
          self.llm=Llm(system=self.system_prompt, tools=registry.schemas())
          self.task_queue=queue.Queue(maxsize=10)

     def enqueue(self,task):
          self.task_queue.put_nowait(task)

     def takeTask(self):
          return self.task_queue.get_nowait()

     def reset(self):
          self.llm.reset()

     def loop(self):
          task = self.takeTask()
          print("taking task:",task.to_string())
          self.llm.reset()
          
          self.llm.add_user(
               f"Achieve Your Goal For Below Task"
               f"{task.to_string()}"
          )
          done=False
          while self.llm.tokens_used < self.max_tokens:
               response=self.llm.ask()
               self.llm.add_message(response)
               for call in (response.tool_calls or []):
                    name=call.function.name
                    args=json.loads(call.function.arguments) if call.function.arguments else {}
                    result=self.registry.run(name, **args)
                    self.llm.add_tool_result(call.id, json.dumps(result))
                    if name == "stop":
                         done=True
                         break
               if done:
                    break

          if done:
               print("model completed by calling stop method")
          else:
               print(f"TOKEN budget reached: ({self.max_tokens}). tokens used: {self.llm.tokens_used}")


