import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from lesson.lesson2_function_call.tools import customer_tools,get_weather

env_file=Path(__file__).resolve().parent.parent/'.env'
# print(env_file)

load_dotenv(dotenv_path=env_file, verbose=True)

API_KEY= os.getenv("API_KEY")
MODEL =os.getenv("MODEL")
BASE_URL =os.getenv("BASE_URL")

chat_history=[]

client = OpenAI(base_url=BASE_URL,api_key=API_KEY)
def chat(prompt:str) ->str:
    chat_history.append({"role":"user", "content":prompt})
    response= client.chat.completions.create(
        model=MODEL,
        messages=chat_history
        # tools=customer_tools,
        # tool_choice="auto"
    )

    result = response.choices[0].message.content.strip()
    print(f"ai:{result}")
    chat_history.append({"role":"assistant","content":result})
    return result


if __name__=="__main__":

    while True:
        user_prompt = input("用户：")
        if user_prompt=="quit":
            print("退出，会话结束")
            break
        ai_response=chat(user_prompt)


