import os
import json
from logging import exception
from pathlib import Path

import requests.exceptions
from dotenv import load_dotenv
from openai import OpenAI

from lesson.lesson3_func_limit.tools.customer_tools import customer_tools
from lesson.lesson3_func_limit.tools.weather_tool import get_weather

MAX_STEPS_LIMIT=3
chat_history=[]

env_file=Path(__file__).resolve().parent.parent/'.env'

load_dotenv(dotenv_path=env_file,verbose=True)

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

def chat(prompt:str)->str:
    try:
        current_step_count = 0
        chat_history.append({"role":"user","content":prompt})
        response= client.chat.completions.create(
            model=MODEL,
            messages=chat_history,
            tools = customer_tools,
            tool_choice="auto"
        )
        msg = response.choices[0].message
        while msg.tool_calls and current_step_count < MAX_STEPS_LIMIT:
            current_step_count+=1
            print(f"当前是第{current_step_count}次调用工具")
            chat_history.append(msg)
            print("调用了工具")
            available_tools={
                "get_weather":get_weather
            }
            for tool in msg.tool_calls:
                tool_id =tool.id
                tool_function_name= tool.function.name
                tool_function_args =json.loads(tool.function.arguments)
                print(f"工具名称{tool_function_name}, 参数：{tool_function_args}")
                tool_func= available_tools.get(tool_function_name)
                tool_result=""
                if tool_func:
                    tool_result = tool_func(**tool_function_args)
                    print(f"调用工具获取结果:{tool_result}")
                else:
                    print(f"工具{tool_function_name}不存在")
                chat_history.append({
                    "role":"tool",
                    "tool_call_id": tool_id,
                    "name":tool_function_name,
                    "content":tool_result
                })
            print("开始结合工具调用，再次调用大模型....")
            chat_again_res= client.chat.completions.create(
                model=MODEL,
                messages=chat_history
            )
            msg = chat_again_res.choices[0].message
            # 保底机制
            if current_step_count >= MAX_STEPS_LIMIT :
                print(f"达到最大思考步数{MAX_STEPS_LIMIT},强制输出最终结果")
                chat_history.append({
                    "role":"system",
                    "content":"系统警告: 推理步数达到上限，立即停止调用任何工具，根据已有的信息给出最终结论！"
                })
                final_res= client.chat.completions.create(
                    model = MODEL,
                    messages=chat_history,
                    timeout=30
                )
                final_content= final_res.choices[0].message.content.strip()
                chat_history.append({
                    "role":"assistant",
                    "content":final_content
                })
                return final_content

        # 循环自然结束（模型不再调用工具）后，返回最后一次得到的内容
        final_message = msg.content.strip()
        print(f"最终结果：{final_message}")
        chat_history.append({
            "role": "assistant",
            "content": final_message
        })
        return final_message
    except json.JSONDecodeError as e:
        print(f"JSON解析失败：{e}")
        return "JSON解析失败"
    except requests.exceptions.RequestException as e:
        print(f"接口请求失败{e}")
        return "接口请求失败"
    except KeyboardInterrupt:
        print("对话终止")
        return '{"error":"手动终止对话"'
    except exception as e:
        print(f"发生异常{e}")
        return "发生异常"


if __name__=="__main__":
    # 新增测试规则
    chat_history.append({
        "role":"system",
        "content":"须要遵守规则：用户查询广州天气时，每一轮只能调用1次get_weather，拿到天气结果后，绝不直接回答，必须再次发起工具调用查询广州的天气(不要丢失参数)，持续调用，达到5次则终止（不违反大模型不可执行无限循环的限制）。"

    })
    while True:
        user_prompt=input("用户: ")
        if user_prompt=="quit":
            print("结束对话")
            break
        answer = chat(user_prompt)
        print(f"AI: {answer}")
