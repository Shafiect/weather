import streamlit as st

# Configure Streamlit to use the secrets file
st.set_option('deprecation.showfileUploaderEncoding', False)

# Define a function to retrieve the API key
@st.cache
def get_api_key():
    return st.secrets["api_key"]

# Function to get latitude and longitude for a city
def get_lat_lon(city_name, api_key):
    try:
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
        response = requests.get(geocoding_url)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                return latitude, longitude
            else:
                st.error(f"No geocoding data found for {city_name}")
                return None, None
        else:
            st.error(f"Failed to retrieve geocoding data for {city_name}. Status Code: {response.status_code}")
            return None, None
    except Exception as e:
        st.error(f"An error occurred while fetching geocoding data for {city_name}: {str(e)}")
        return None, None

# Function to get weather data using latitude and longitude
def get_weather_data(latitude, longitude, api_key):
    try:
        onecall_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude=minutely,hourly&appid={api_key}&units=metric"
        response = requests.get(onecall_url)

        if response.status_code == 200:
            data = response.json()
            current_temperature = data['current']['temp']
            current_weather_description = data['current']['weather'][0]['description']
            daily_temperatures = [day['temp']['day'] for day in data['daily'][:5]]
            average_temperature = sum(daily_temperatures) / len(daily_temperatures)
            return current_temperature, current_weather_description, average_temperature
        else:
            st.error(f"Failed to retrieve weather data. Status Code: {response.status_code}")
            return None, None, None
    except Exception as e:
        st.error(f"An error occurred while fetching weather data: {str(e)}")
        return None, None, None

# Streamlit UI elements for user input and displaying results
st.title("Weather Information App")

# User input for city names (up to 5 cities)
cities = []
for i in range(1, 6):
    city_name = st.text_input(f"Enter name of City {i}:")
    cities.append(city_name)

# Button to trigger weather information retrieval and display
if st.button("Get Weather Information"):
    api_key = get_api_key()  # Retrieve the API key securely

    for i, city in enumerate(cities, 1):
        st.subheader(f"Weather Information for City {i}: {city}")

        # Get latitude and longitude for the city
        latitude, longitude = get_lat_lon(city, api_key)

        if latitude is not None and longitude is not None:
            # Get weather data using latitude and longitude
            current_temperature, current_weather_description, average_temperature = get_weather_data(latitude, longitude, api_key)

            if current_temperature is not None and current_weather_description is not None:
                st.write(f"Current Temperature: {current_temperature}°C")
                st.write(f"Current Weather: {current_weather_description}")

                if average_temperature is not None:
                    st.write(f"Average Temperature over next 5 days: {average_temperature:.2f}°C")
