from pydantic import BaseModel, Field
from typing import Type, Callable, Any

class Tool:
     def __init__(self, name:str, description:str, args_schema: Type[BaseModel], func: Callable[...,Any]):
          self.name=name
          self.description=description
          self.args_schema= args_schema
          self.func=func

     def schema(self):
          return{
               "name": self.name,
               "description": self.description,
               "parameters":self.args_schema.model_json_schema()
          }
     def run(self, **kwargs):
          validated_args=self.args_schema(**kwargs)
          return self.func(**validated_args.model_dump())