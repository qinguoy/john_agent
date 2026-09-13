import json
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
        messages=chat_history,
        tools=customer_tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        chat_history.append(msg)
        print(f"AI调用了工具")
        available_tools= {
            "get_weather":get_weather
        }
        for tool in msg.tool_calls:
            tool_id =tool.id
            tool_function_name =tool.function.name
            tool_function_args =json.loads(tool.function.arguments)
            print(f"工具名称：{tool_function_name}, 参数： {tool_function_args}")
            tool_func= available_tools.get(tool_function_name)
            tool_result=""
            if tool_func:
                tool_result = tool_func(**tool_function_args)
                print(tool_result)
            else:
                print(f"工具{tool_function_name} 不存在")
            chat_history.append({
                "role":"tool",
                "tool_call_id":tool_id,
                "name":tool_function_name,
                "content":tool_result
            })
        print("正在结合工具调用，生成最终结果")
        chat_again_res= client.chat.completions.create(
            model=MODEL,
            messages= chat_history
        )
        final_msg = chat_again_res.choices[0].message.content.strip()
        chat_history.append({
            "role":"assistant",
            "content":"final_msg"
        })
        print("调用工具结束")
        return final_msg
    else:
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
        print(ai_response)


