from tools.Tool import Tool
from typing import Dict

class ToolsRegistry:
     def __init__(self):
          self._tools:Dict[str, Tool] = {}
     def add_tool(self, tool:Tool):
          self._tools[tool.name] = tool
     def get_tools(self):
          return [tool.schema() for tool in self._tools.values()]
     