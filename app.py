from flask import Flask, render_template, request
import requests
from collections import defaultdict, Counter

app = Flask(__name__)

API_KEY = "d22b046573cca4a01287e88d0b107be4"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(weather_url)
                data = response.json()
                if response.status_code == 200:
                    lat = data["coord"]["lat"]
                    lon = data["coord"]["lon"]

                    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
                    aqi_response = requests.get(aqi_url).json()
                    aqi = aqi_response["list"][0]["main"]["aqi"]
                    aqi_meaning = {
                        1: "Good",
                        2: "Fair",
                        3: "Moderate",
                        4: "Poor",
                        5: "Very Poor"
                    }.get(aqi, "Unknown")

                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"],
                        "aqi": aqi,
                        "aqi_text": aqi_meaning
                    }
                else:
                    error = data.get("message", "Unknown error")
            except Exception as e:
                error = str(e)

    return render_template("index.html", weather=weather_data, error=error)


@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    forecast_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
                geo_response = requests.get(geo_url).json()

                if len(geo_response) == 0:
                    error = "City not found"
                else:
                    lat = geo_response[0]["lat"]
                    lon = geo_response[0]["lon"]

                    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
                    forecast_response = requests.get(forecast_url).json()

                    if forecast_response.get("cod") == "200":
                        daily_forecast = defaultdict(list)
                        for entry in forecast_response["list"]:
                            date_str = entry["dt_txt"].split(" ")[0]
                            daily_forecast[date_str].append({
                                "time": entry["dt_txt"].split(" ")[1][0:5],
                                "temp": entry["main"]["temp"],
                                "description": entry["weather"][0]["description"],
                                "icon": entry["weather"][0]["icon"],
                            })

                        forecast_data = []
                        from datetime import datetime

                        for date, items in daily_forecast.items():
                            avg_temp = sum(item["temp"] for item in items) / len(items)
                            descriptions = [item["description"] for item in items]
                            common_desc = Counter(descriptions).most_common(1)[0][0]
                            date_obj = datetime.strptime(date, "%Y-%m-%d")
                            day_name = date_obj.strftime("%A")  # Pazartesi, Salı ... (İngilizce)

                            forecast_data.append({
                                "date": date,
                                "day_name": day_name,
                                "avg_temp": round(avg_temp, 1),
                                "common_desc": common_desc,
                                "hours": items
                            })

                        forecast_data.sort(key=lambda x: x["date"])
                    else:
                        error = forecast_response.get("message", "Failed to get forecast data")
            except Exception as e:
                error = str(e)

    return render_template("forecast.html", forecast=forecast_data, error=error)


if __name__ == "__main__":
    app.run(debug=True)
