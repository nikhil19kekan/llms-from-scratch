from pydantic import BaseModel
from tools.Tool import Tool
class ToolRegistry:
     class StopArgs(BaseModel):
               pass
     stop:Tool = Tool(
          name="stop",
          description="Signals that the task is fully complete and ends the run. Call it in the SAME turn right after you finish the task. Do not call it before you have delivered the task, and never keep working after calling it.",
          args_schema=StopArgs,
          isReadOnly=False,
          func=lambda: "acknowledged, stopping"
     )
     def __init__(self):
          self._tools = {"stop": self.stop}
          
     def register(self, tool):
          self._tools[tool.name] = tool
          return tool

     def get(self, name):
          return self._tools[name]

     def all(self):
          return list(self._tools.values())

     def schemas(self):
          return [{"type": "function", "function": tool.schema()} for tool in self.all()]

     def run(self, name, **kwargs):
          return self.get(name).run(**kwargs)
