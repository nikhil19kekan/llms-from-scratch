
import os
from dotenv import load_dotenv
from core.jev_basic import Question
from core.llm import Llm
import json
from core.jev_basic import Jev
import asyncio
from agents.SiteReliabilityEngineer.incident import Incident
from core.agent import Agent
from agents.SiteReliabilityEngineer.sre_tools import registry
from utils.utils import load_data

load_dotenv()

MODEL = os.environ["LLM_MODEL"]
_INCIDENTS_DATA_PATH = os.path.join(os.path.dirname(__file__), "./agents/SiteReliabilityEngineer/data/incidents.json")


def main():
    sreAgent:Agent = Agent(
        systemPrompt="You are an SRE triaging ONE incident: find the problem, its root cause, and the fix. You only diagnose and report, you cannot apply changes. Logs are the source of truth. You work within a limited token budget: investigate directly, keep each reasoning note to one or two sentences, never repeat a call with the same arguments, and never ask the human. As soon as you know the problem, root cause, and fix, call sendMessage ONCE with a concise triage and call stop in the same turn.",
        maxTokens=10000,
        registry=registry
    )
    incs:list[Incident] = [Incident.from_dict(i) for i in load_data(_INCIDENTS_DATA_PATH)["incidents"]]
    # for inc in incs:
    sreAgent.enqueue(incs[0])
    sreAgent.loop()

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
