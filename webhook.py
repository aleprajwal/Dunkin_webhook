from flask import Flask, request, make_response
from flask_mysqldb import MySQL
import cart
import logging
import json
import os

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

    # action to adds drinks item in cart
    if action == 'order.items.drinks':
        params = req.get('queryResult').get('parameters')
        try:
            for a, s, d in zip(params['number'], params['size'], params['drink']):
                item = cart.Drinks_Item(d, s, int(a))
                bag.drinks_update(item)

            response = {'fulfillmentText': 'Anything else?'}
            res = json.dumps(response, indent=4)
            r = make_response(res)
            return r
        except Exception as e:
            logging.error('500 Error  --> order.items.drinks intent', exc_info=True)

    # action to adds bakery item in cart
    if action == 'order.items.bakery':
        params = req.get('queryResult').get('parameters')
        try:
            for n, b in zip(params['number'], params['bakery']):
                item = cart.Bakery_Item(b, int(n))
                bag.bakery_update(item)
            response = {'fulfillmentText': 'Anything else?'}
            res = json.dumps(response, indent=4)
            r = make_response(res)
            return r
        except Exception as e:
            logging.error('500 Error  --> order.items.bakery intent', exc_info=True)

    # action to shows ordered item list available in cart
    if action == 'order.items.check':
        try:
            if not bag.show_items():
                response = {'fulfillmentText': 'Your order list is empty. You can order drinks and bakery items.'}
                res = json.dumps(response, indent=4)
                r = make_response(res)
                return r
            else:
                response = {'fulfillmentText': 'Order List:\n{}\nWould you want to checkout?'.
                    format(','.join(item for item in bag.show_items()))}
                res = json.dumps(response, indent=4)
                r = make_response(res)
                return r
        except Exception as e:
            logging.error('500 Error --> order.product.check intent', exc_info=True)

    # action to remove selected item from cart
    if action == 'order.items.remove':
        params = req.get('queryResult').get('parameters')
        try:
            remove_item = params['bakery']
            if params['drink']:
                remove_item = params['size'] + ' ' + params['drink']
            try:
                bag.remove_item(remove_item)
                if bag.show_items():
                    response = {'fulfillmentText': '{} removed from your order list!!\nItems in your order list:\n{}'.
                        format(remove_item, ','.join(item for item in bag.show_items()))}
                else:
                    response = {'fulfillmentText': '{} removed from your order list!!\n Your order list is empty. '
                                                   'You can make an order for drinks and bakery items.'.format(
                        remove_item)}
            except Exception:
                response = {'fulfillmentText': '{} not in your order list!!'.format(remove_item)}

            res = json.dumps(response, indent=4)
            r = make_response(res)
            return r
        except Exception as e:
            logging.error('500 Error --> order.items.remove intent', exc_info=True)

    # action to checkout
    if action == 'order.checkout.custom':
        try:
            cursor = mysql.connection.cursor()
            for _, v in bag.drinks_content.iteritems():
                name = v.name
                size = v.size
                qty = v.qty
                cursor.execute("INSERT INTO OrderDrinks(name, size, qty) VALUES ('{}','{}', {})".format(name, size, qty))
                mysql.connection.commit()
            cursor.close()
            response = {'fulfillmentText': 'Your order is placed. Have a Good day!'}
            res = json.dumps(response)
            r = make_response(res)
            return r

        except Exception:
            logging.error('500 Error --> order.checkout.custom intent', exc_info=True)

    # action to cancel order
    if action == 'order.cancel':
        try:
            bag.clean_cart()
            response = {'fulfillmentText': 'Your order is cancelled.'}
            res = json.dumps(response)
            r = make_response(res)
            return r
        except:
            logging.error('500 Error --> order.cancel intent', exc_info=True)


# run app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
