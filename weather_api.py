from flask import Flask, request, make_response
import logging
import json
import os

host = ''
wwoApiKey = '7ce567a627504e3c82951314192404'
city = 'kathmandu'

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def weather_api():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'JSON Error'

def weather_info():
    path = '{}/premium/v1/weather.ashx?format=json&num_of_days=1&key={}&q={}'.format(host, wwoApiKey, city)

# run app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
