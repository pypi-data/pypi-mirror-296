import json
from langchain_openai import ChatOpenAI
from .base import import_tools
from .agent import run_agent, Runnable, INPUT_MESSAGE, output
import asyncio
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pycoze import utils


params = utils.arg.read_params()
llm_file = params["appPath"] + "/JsonStorage/llm.json"


def load_role_setting(bot_setting_file: str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tools(bot_setting_file: str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        role_setting = json.load(f)

    tools = []
    for tool_id in role_setting["tools"]:
        tools.extend(import_tools(tool_id))
    return tools


def chat(bot_setting_file: str):

    while True:
        input_text = input()
        role_setting = load_role_setting(bot_setting_file)
        tools = load_tools(bot_setting_file)
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        messages = json.loads(input_text[len(INPUT_MESSAGE) :])

        with open(llm_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            chat = ChatOpenAI(
                api_key=cfg["apiKey"],
                base_url=cfg["baseURL"],
                model=cfg["model"],
                temperature=role_setting["temperature"],
            )

        agent = Runnable(
            agent_execution_mode="FuncCall",  # 'FuncCall' or 'ReAct'，大模型支持FuncCall的话就用FuncCall
            tools=tools,
            llm=chat,
            assistant_message=role_setting["prompt"],
        )
        history = []
        for message in messages:
            if message["role"] == "assistant":
                history += [AIMessage(content=message["content"])]
            elif message["role"] == "user":
                history += [HumanMessage(content=message["content"])]
            elif message["role"] == "system":
                history += [SystemMessage(content=message["content"])]
            else:
                raise ValueError("Invalid message")
        result = asyncio.run(run_agent(agent, history))
        output("assistant", result, history)
