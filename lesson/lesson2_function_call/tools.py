import requests

customer_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如北京，上海，广州"
                    }
                }
            }
        }
    }
]


def get_weather(city: str) -> str:
    url=f"https://wttr.in/{city}?format=j1"
    try:
        response= requests.get(url)
        response.raise_for_status()
        data = response.json()
        current_condition =data["current_condition"][0]
        weather_desc= current_condition["weatherDesc"][0]["value"]
        temp_c=current_condition["temp_c"]
        return f"{city} {weather_desc} - {temp_c}℃"
    except Exception as e:
        print(f"Error fetch weahter for {city}, {e}")
        return "调用天气工具失败！"
