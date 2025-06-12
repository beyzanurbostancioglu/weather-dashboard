import requests

API_KEY = "ee159b8a51669c632080efadec947dfc"
city = "London"
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(weather_url)
print(response.status_code)
print(response.json())
