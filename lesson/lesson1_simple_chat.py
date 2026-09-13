import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY= os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL =os.getenv("BASE_URL")

chat_history=[]

# print(API_KEY, MODEL,BASE_URL)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
def chat(prompt):
    try:
        res= client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role":"user",
                "content":prompt
            }]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print(f"Chat error:{e}")
        return "Internal error"


def chat_with_history(user_prompt):
    try:
        if len(user_prompt)<1:
            return
        chat_history.append({"role":"user","content":user_prompt})
        res=client.chat.completions.create(
            model=MODEL,
            messages=chat_history
        )
        res_message = res.choices[0].message.content.strip()
        chat_history.append({"role":"assistant","content":res_message})
        return res_message
    except Exception as e:
        print(f"Chat occurs error, {e}")
        return "Chat occurs error"

def chat_res_json(prompt: str):
    try:
        if len(prompt)<1:
            return
        chat_history.append({"role":"user","content":prompt})
        res = client.chat.completions.create(
            model=MODEL,
            messages= chat_history,
            response_format={"type":"json_object"}
        )
        res_message = res.choices[0].message.content.strip()
        chat_history.append({"role":"assistant","content":res_message})
        return res_message
    except Exception as e:
        print(f"Chat occurs error,{e}")
        return "Chat occurs error"



if __name__=="__main__":

    # ##多轮对话###
    # print("简单的AI对话，输入quit退出")
    # while True:
    #     user_prompt=input("用户:")
    #     if user_prompt=="quit":
    #         print("对话结束")
    #         break
    #     response = chat(user_prompt)
    #     print(f"AI回复：{response}")

    ###多轮历史对话###
    # while True:
    #     user_prompt=input("用户：")
    #     if user_prompt=="quit":
    #         print("对话结束")
    #         break
    #     response=chat_with_history(user_prompt)
    #     print(f"AI回复：{response}")


    # ###添加系统提示词###
    # chat_history.append({
    #     "role":"system",
    #     "content":"你是一个资深的软件架构师"
    # })
    # while True:
    #     user_prompt=input("用户：")
    #     if user_prompt=="quit":
    #         print("对话结束")
    #         break
    #     response=chat_with_history(user_prompt)
    #     print(f"AI回复：{response}")

    ##### chat response format:json
    chat_history.append({"role":"system","content":"你是一个高级java系统架构师"})
    while True:
        user_prompt =input("用户：")
        if user_prompt == "quit":
            print("会话结束")
            break
        response_message =chat_res_json(user_prompt)
        print(f"AI:{response_message}")

