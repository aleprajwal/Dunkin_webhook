import logging
import cart
import json
from weather_info import weather_info
from response import SUNNY_WEATHER, COOL_WEATHER
from flask import make_response


class ActionHandler:
    def __init__(self, req, bag):
        self.req = req
        self.bag = bag

    # action to adds drinks item in cart
    def order_items_drinks(self):
        params = self.req.get('queryResult').get('parameters')
        try:
            if type(params['number']) is not list:
                item = cart.Drinks_Item(params['drink'][0], params['size'][0], int(params['number']))
                self.bag.drinks_update(item)
            else:
                for a, s, d in zip(params['number'], params['size'], params['drink']):
                    item = cart.Drinks_Item(d, s, int(a))
                    self.bag.drinks_update(item)

            response = {'fulfillmentText': 'Anything else?'}
            if not self.bag.bakery_content:  # check if bakery item is not ordered yet
                response = {'fulfillmentText': 'You can make order for bakery items. What can I get for you?'}
            res = json.dumps(response, indent=4)
            r = make_response(res)
            return r
        except Exception as e:
            logging.error('500 Error  --> order.items.drinks intent', exc_info=True)

    # action to adds bakery item in cart
    def order_items_bakery(self):
        params = self.req.get('queryResult').get('parameters')
        try:
            if type(params['number']) is not list:
                item = cart.Bakery_Item(params['bakery'][0], int(params['number']))
                self.bag.bakery_update(item)
            else:
                for n, b in zip(params['number'], params['bakery']):
                    item = cart.Bakery_Item(b, int(n))
                    self.bag.bakery_update(item)
            response = {'fulfillmentText': 'Anything else?'}
            if not self.bag.drinks_content:
                response = {'fulfillmentText': 'You can make order for drinks. What can I get for you?'}
            res = json.dumps(response, indent=4)
            r = make_response(res)
            return r
        except Exception as e:
            logging.error('500 Error  --> order.items.bakery intent', exc_info=True)

    # action to shows ordered item list available in cart
    def order_items_check(self):
        try:
            if not self.bag.show_items():
                response = {'fulfillmentText': 'Your order list is empty. You can order drinks and bakery items.'}
                res = json.dumps(response, indent=4)
                r = make_response(res)
                return r
            else:
                # response = {'fulfillmentText': 'Order List:\n{}\nWould you want to checkout?'.
                #     format(','.join(item for item in bag.show_items()))}
                temp = weather_info()
                if int(temp) >= 32: # concept -> recommend items which are not in order list w.r.t weather condition
                    response = {'fulfillmentText': SUNNY_WEATHER.format(
                        orderList=','.join(item for item in bag.show_items()),
                        temp=temp)}
                else:
                    response = {'fulfillmentText': COOL_WEATHER.format(
                        orderList=','.join(item for item in bag.show_items()),
                        temp=temp)}
                res = json.dumps(response, indent=4)
                r = make_response(res)
                return r

        except Exception as e:
            logging.error('500 Error --> order.product.check intent', exc_info=True)

    # action to uosell items
    def order_items_checkUpsell(self):
        params = self.req.get('queryResult').get('parameters')
        try:
            if type(params['number']) is not list:
                item = cart.Drinks_Item(params['drink'][0], params['size'][0], int(params['number']))
                self.bag.drinks_update(item)
            else:
                for a, s, d in zip(params['number'], params['size'], params['drink']):
                    item = cart.Drinks_Item(d, s, int(a))
                    self.bag.drinks_update(item)
            response = {'fulfillmentText': 'Your Order List:\n{}\nWould you want to checkout or cancel order?'.format(
                ','.join(item for item in self.bag.show_items()))}
            res = json.dumps(response)
            r = make_response(res)
            return r
        except Exception:
            logging.error('500 Error --> order.items.check.upsell intent', exc_info=True)

    # action to remove selected item from cart
    def order_items_remove(self):
        params = self.req.get('queryResult').get('parameters')
        try:
            remove_item = params['bakery']
            if params['drink']:
                remove_item = params['size'] + ' ' + params['drink']
            try:
                self.bag.remove_item(remove_item)
                if self.bag.show_items():
                    response = {'fulfillmentText': '{} removed from your order list!!\nItems in your order list:\n{}'.
                        format(remove_item, ','.join(item for item in self.bag.show_items()))}
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

    # action to cancel order
    def order_cancel(self):
        try:
            self.bag.clean_cart()
            response = {'fulfillmentText': 'Your order is cancelled.'}
            res = json.dumps(response)
            r = make_response(res)
            return r
        except:
            logging.error('500 Error --> order.cancel intent', exc_info=True)

    # action to checkout and insert order into database
    def order_checkout_custom(self):
        try:
            cursor = mysql.connection.cursor()
            for _, v in self.bag.drinks_content.iteritems():
                name = v.name
                size = v.size
                qty = v.qty
                cursor.execute("INSERT INTO OrderDrinks(name, size, qty) VALUES ('{}','{}', {})".format(name, size, qty))
                mysql.connection.commit()
            for _, v in self.bag.bakery_content.iteritems():
                name = v.name
                qty = v.qty
                cursor.execute("INSERT INTO OrderBakery(name, qty) VALUES ('{}', {})".format(name, qty))
                mysql.connection.commit()
            cursor.close()
            response = {'fulfillmentText': 'Your order is placed. Have a Good day!'}
            res = json.dumps(response)
            r = make_response(res)
            return r
        except:
            logging.error('500 Error --> order.checkout.custom intent', exc_info=True)
