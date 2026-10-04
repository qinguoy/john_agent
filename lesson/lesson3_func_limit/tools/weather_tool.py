import requests

def get_weather(city: str) -> str:
    url=f"https://wttr.in/{city}?format=j1"
    try:
        response= requests.get(url)
        response.raise_for_status()
        data = response.json()
        current_condition =data["current_condition"][0]
        print(current_condition)
        weather_desc= current_condition["weatherDesc"][0]["value"]

        temp_c=current_condition["temp_C"]
        return f"{city} {weather_desc} - {temp_c}℃"
    except Exception as e:
        print(f"Error fetch weahter for {city}, {e}")
        return "调用天气工具失败！"