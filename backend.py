import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather_data(place, forcecast_days=5):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    content = response.json()
    data = content["list"]
    nr_values = 8 * forcecast_days
    data = data[:nr_values]
    
    #temperatures = [content["list"][i]["main"]["temp"] for i in range(len(content["list"]))]
    #temperatures = [temperatures/ 10 for temperatures in temperatures]
        
    #sky = [content["list"][i]["weather"][0]["main"] for i in range(len(content["list"]))]
    #print(sky)
    return data






if __name__ == "__main__":
    get_weather_data(place="Delhi")
