class Drinks_Item(object):
    def __init__(self, name, size, qty):
        self.name = name
        self.size = size
        self.qty = qty


class Bakery_Item(object):
    def __init__(self, name, qty, *args):
        self.name = name
        self.qty = qty


class Cart(object):
    def __init__(self):
        self.drinks_content = dict()  # store details of ordered drinks items
        self.bakery_content = dict()  # store details of ordreed bakery items

    # update drinks order in cart
    def drinks_update(self, item):
        name = item.size + ' ' + item.name  # creating key(name) with size and name of item
        if name not in self.drinks_content:  # check if ordered drink item is perviously added
            self.drinks_content.update({name: item})  # adding drinks item in drinks_content dictonary with name as key
            return
        self.drinks_content.get(name).qty += item.qty  # if drinks is previously ordered, only increase its quantity

    # update bakery item order in cart
    # steps are similar to drinks_update()
    def bakery_update(self, item):
        name = item.name
        if name not in self.bakery_content:
            self.bakery_content.update({name: item})
            return
        self.bakery_content.get(name).qty += item.qty

    # show items available in cart
    def show_items(self):
        item_list = list()
        for _, v in self.drinks_content.iteritems():  # loop through items available in drinks_content
            res = '{} {} {}'.format(v.qty, v.size, v.name)  # creating a proper response eg. 2 large coffee
            item_list.append(res)
        for _, v in self.bakery_content.iteritems():
            res = '{} {}'.format(v.qty, v.name)  # eg. 5 Donut
            item_list.append(res)
        return item_list  # return list of ordered items

    # remove selected items from cart
    def remove_item(self, key):
        if key in self.drinks_content:
            self.drinks_content.pop(key)
        else:
            self.bakery_content.pop(key)

    # clear all items available in cart
    def clean_cart(self):
        self.drinks_content.clear()
        self.bakery_content.clear()
