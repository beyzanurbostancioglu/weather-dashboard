from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "d22b046573cca4a01287e88d0b107be4"


# geçici olarak buraya yaz


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
                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"]
                    }
                else:
                    error = data.get("message", "Bilinmeyen hata")
            except Exception as e:
                error = str(e)

    return render_template("index.html", weather=weather_data, error=error)


if __name__ == "__main__":
    app.run(debug=True)
