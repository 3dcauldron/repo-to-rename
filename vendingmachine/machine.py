class Machine(object):

    def __init__(self,product={},size=0,quantity=0,price=0.0,key = {'id':'01AB', 'user':'TEST'}, change = 0):
        self.product = product
        self.size = size
        self.quantity = quantity
        self.price = price
        self.key = key
        self.change = change

    def update_product(self,product):
        self.product = product

    def update_size(self,size):
        self.size = size

    def update_quantity(self,quantity):
        self.quantity = quantity

    def update_price(self,price):
        self.price = price

    def update_key(self,key):
        self.key = key

    def update_change(self,coin,newAmount):
        self.change = newAmount

    def get_user(self):
        return self.key['user']

    def to_dict(self):
        t = {}
        t['product'] = self.product
        t['size'] = self.size
        t['quantity'] = self.quantity
        t['price'] = self.price
        t['key'] = self.key
        t['change'] = self.change
        return t
