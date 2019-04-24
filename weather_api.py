import requests

host = 'api.worldweatheronline.com'
wwoApiKey = '7ce567a627504e3c82951314192404'
city = 'kathmandu'


def weather_info():
    path = 'https://{}/premium/v1/weather.ashx?format=json&num_of_days=1&key={}&q={}'.format(host, wwoApiKey, city)
    json_res = requests.get(path).json()
    temp_C = json_res['data']['current_condition'][0]['temp_C']
    return temp_C


def weather_stat(temp_C):
    if temp_C > 35:
        response = 'sunny'


if __name__ == '__main__':
    print weather_info()
