from flask import Flask, request, make_response
from flask_mysqldb import MySQL
import cart
from action_handler import ActionHandler
import logging
import json
import os

from weather_info import weather_info
from response import COOL_WEATHER, SUNNY_WEATHER

# initilize flask app
app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'phpmyadmin'
app.config['MYSQL_PASSWORD'] = 'P@ssw0rd'
app.config['MYSQL_DB'] = 'DunkinDonuts'

mysql = MySQL(app)

# initilize cart
bag = cart.Cart()


@app.route('/', methods=['POST', 'GET'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'JSON Error'

    action_handler = ActionHandler(req, bag)
    action_dic = {'order.items.drinks': action_handler.order_items_drinks(),
                  'order.items.bakery': action_handler.order_items_bakery(),
                  'order.items.check': action_handler.order_items_check()}
    action_dic[action]


# run app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
