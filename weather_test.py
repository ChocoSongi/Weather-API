import requests

# IP 주소 기반 위치 정보를 가져오는 함수 (ipinfo.io API 사용)
def get_location_from_ip():
    response = requests.get('http://ipinfo.io/')
    data = response.json()
    return data['city'], data['region'], data['country']

# OpenWeatherMap API를 통해 위도/경도로 변환한 후 날씨 정보를 가져오는 함수
def get_weather(city):
    api_key = '34ca17f9b51486bfaeaf8d66c7fde8fd'  # OpenWeatherMap API 키 입력

    # 1. 도시명을 위도와 경도로 변환 (Geocoding API 사용)
    geo_api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_api_url)
    geo_data = geo_response.json()

    if len(geo_data) == 0:
        print(f"{city}의 위도와 경도를 찾을 수 없습니다.")
        return None

    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']

    # 2. 위도와 경도를 사용하여 날씨 정보 요청 (Weather API 사용)
    weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_api_url)
    weather_data = weather_response.json()

    # 날씨 정보 출력
    if weather_data['cod'] == 200:
        main = weather_data['main']
        temperature = main['temp']
        humidity = main['humidity']
        return temperature, humidity
    else:
        print(f"날씨 정보를 가져오는 데 실패했습니다: {weather_data['message']}")
        return None

# 메인 실행 함수
def main():
    city, region, country = get_location_from_ip()
    print(f"현재 IP 기반 위치: {city}, {region}, {country}")
    
    weather_data = get_weather(city)
    
    if weather_data:
        temperature, humidity = weather_data
        print(f"현재 {city}의 기온: {temperature}°C, 습도: {humidity}%")
    else:
        print("날씨 데이터를 가져올 수 없습니다.")

if __name__ == "__main__":
    main()