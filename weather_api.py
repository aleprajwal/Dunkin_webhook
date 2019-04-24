from flask import Flask, request, make_response
import logging
import json
import os

host = ''
wwoApiKey = ''
city = 'kathmandu'

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def weather():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'JSON Error'


# run app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
