# Weather & Air Quality Dashboard 🌤️

A simple Flask app that provides current weather and air quality info for any city, plus a 5-day forecast — with a clean, user-friendly interface.

---

## Features

- Search current weather by city name  
- Display temperature, description & weather icons  
- 5-day weather forecast with daily summaries and hourly details  
- Error handling for invalid city names or API issues  
- Responsive design using Tailwind CSS  

---

## Technologies Used

- Python 3.x  
- Flask  
- Requests  
- OpenWeatherMap API  
- Tailwind CSS (via CDN)  

---

## Setup & Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```
   
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
4. Get your OpenWeatherMap API key from https://openweathermap.org/api

5. Add your API key in app.py:
 ```bash
   API_KEY = "your_api_key_here"
   ```

6. Run the app:

   ```bash
   python app.py
   ```
## Usage
-Enter a city name and click Get Weather

-View current weather and a detailed 5-day forecast

-Error messages show if city not found

