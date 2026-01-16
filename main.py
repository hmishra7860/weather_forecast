import streamlit as st
import plotly.express as px
from backend import get_weather_data

#------------------------Streamlit App-----------------------#


st.title("Weather Forecast Dashboard")
place = st.text_input("Place")

days = st.slider("Days of Forecast", min_value=1, max_value=5, help="Select number of days for weather forecast")       

kind = st.selectbox("Select date to view the forecast",("temperature", "Sky"))

st.subheader(f"Weather forecast for {place} for next {days} days")



#------------------------Fetch Weather Data-----------------------#

if place:

    try:

            weather_data = get_weather_data(place, days)



            #-----------------------Temperature Plotting-----------------------#

            if kind == "temperature":
                temperature = [dict["main"]["temp"]/10 for dict in weather_data]
                dates = [dict["dt_txt"] for dict in weather_data]

                print(temperature)
                print(dates)

                figure = px.line(x=dates, y=temperature, labels={"x": "Date", "y": "Temperature (°C)"}, title="Temperature Forecast")
                st.plotly_chart(figure)


            #-----------------------Sky Image Display-----------------------#

            if kind == "Sky":
                images = {"Clear": "clear.png",
                                "Clouds": "cloud.png",
                                "Rain": "rain.png",
                                "Snow": "snow.png",
                        }
                sky_data = [item["weather"][0]["main"] for item in weather_data]
                dates = [item["dt_txt"] for item in weather_data]

                filepaths = [images[data] for data in sky_data]
                st.image(filepaths, caption=dates, width=95)
    except KeyError:
            st.error("Place not found. Please enter a valid place name.")           