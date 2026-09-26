import os
import httpx
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

load_dotenv()
@dataclass
class Question:
    type: str
    instructions: str
    criteria: dict[str, str] | list[str]

class Jev:
    state:str
    questions:list[Question]
    payload:dict
    model:str
    key=str
    endpoint:str
    timeout:int

    def __init__(self, state="", questions=None, model=os.environ["JEV_MODEL"], key=os.environ["JEV_API_KEY"], endpoint=os.environ["JEV_ENDPOINT"], timeout=10):
        self.state=state
        self.questions=questions
        self.model=model
        self.key=key
        self.endpoint=endpoint
        self.timeout=timeout

    def __create_payload(self) -> dict:
        return {
            "model": self.model,
            "state": self.state,
            "questions": {name: asdict(q) for name, q in self.questions.items()},
        }

    def get_response(self):
        return httpx.post(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.key}"},
            json=self.__create_payload(),
            timeout=10)
