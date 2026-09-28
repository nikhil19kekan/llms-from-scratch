import os

import litellm
from dotenv import load_dotenv
from litellm import completion, acompletion

litellm.suppress_debug_info = True

load_dotenv()

class Llm:
    prompt:str
    model:str
    system:str
    context:str
    def __init__(self, prompt="", model=os.environ["LLM_MODEL"], system="", tools=None):
        self.prompt=prompt
        self.model=model
        self.system=system
        self.tools=tools
        self.context=[]
        self.tokens_used=0
        if system:
            self.context.append({"role": "system", "content": system})

    def add_user(self, prompt):
        self.context.append({"role": "user", "content": prompt})

    def add_message(self, message):
        self.context.append(message)

    def add_tool_result(self, tool_call_id, content):
        self.context.append({"role": "tool", "tool_call_id": tool_call_id, "content": content})

    def reset(self):
        self.context = []
        self.tokens_used = 0
        if self.system:
            self.context.append({"role": "system", "content": self.system})


    def ask(self, **options):
        response = completion(
            model=self.model,
            messages=self.context,
            tools=self.tools,
            num_retries=2,
            reasoning_effort='low',
            **options,
        )
        if response.usage:
            self.tokens_used += response.usage.total_tokens
        return response.choices[0].message


    def stream(self, **options):
        chunks = completion(
            model=self.model,
            messages=self.__build_messages(self.prompt, self.system),
            stream=True,
            **options,
        )
        for chunk in chunks:
            text = chunk.choices[0].delta.content
            if text:
                yield text


    async def ask_async(self, **options):
        response = await completion(
            model=self.model,
            messages=self.__build_messages(self.prompt, self.system),
            num_retries=2,
            **options,
        )
        return response.choices[0].message.content


