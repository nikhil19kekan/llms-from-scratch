
import os
from dotenv import load_dotenv
from core.jev_basic import Question
from core.llm import Llm
import json
from core.jev_basic import Jev
import asyncio
from agents.SiteReliabilityEngineer.incident import Incident
from agents.SiteReliabilityEngineer.agent import SreAgent
load_dotenv()

MODEL = os.environ["LLM_MODEL"]


def main():
    sreAgent:SreAgent = SreAgent()
    sreAgent.queueIncident(Incident("the app is behaving flaky today",1,1))
    sreAgent.triage()
    # question="tell an interesting fact in 10 words"
    # llm:Llm=Llm(question)

    # print("one shot response:",llm.ask())

    # print("streaming response")
    # for piece in llm.stream(prompt=question):
    #     print(piece, end="", flush=True)

    # print("async response:",asyncio.run(llm.ask_async()))

    # questions = {
    #     "is_urgent": Question(
    #         type="noul",
    #         instructions="Does this message convey urgency?",
    #         criteria={
    #             "true": "Explicitly time-sensitive",
    #             "false": "No urgency expressed",
    #         },
    #     ),
    #     "department": Question(
    #         type="choice",
    #         instructions="Which team should handle this?",
    #         criteria={
    #             "billing": "Payments, invoicing, refunds",
    #             "technical": "Bugs, outages, integrations",
    #             "sales": "Pricing, upgrades, new accounts",
    #         },
    #     ),
    #     "frustration": Question(
    #         type="score",
    #         instructions="How frustrated is the customer?",
    #         criteria=["Calm", "Frustrated", "Very angry"],
    #     ),
    # }
    # jev: Jev = Jev(state="customers payment is failing", questions=questions)
    # response=jev.get_response()
    # response.raise_for_status()
    # print("jev response",json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
