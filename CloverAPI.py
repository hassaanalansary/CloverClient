import json

import requests


class CloverClient(object):
    def __init__(self, merchant_id, auth_token):
        self.merchant_id = merchant_id
        self.auth_token = auth_token

        self.api_token = '?access_token=' + self.auth_token
        self.base_url = 'https://api.clover.com/v3/merchants/' + self.merchant_id + '/'
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def add_item(self, name: str, price: int,quantity: int = 0, **kwargs):
        if len(name) > 127:  # clover doesnt accept more than 127 characters
            name = name[:127]
        myitem = {'name': name, 'price': price}
        for key in kwargs.keys():
            value = kwargs[key]
            myitem[key] = value

        url = self.base_url + 'items' + self.api_token
        request = requests.post(url, data=json.dumps(myitem), headers=self.headers)

        if request.status_code == 200:
            text = json.loads(request.text)
            if quantity > 0:
                self.add_quantity(text['id'], quantity)
            return [True, text['id']]
        else:
            return [False, request.text]

    def attach_category(self, item_id, category_id):
        url = self.base_url + 'category_items' + self.api_token
        myitem = {'elements': [
            {"item": {"id": item_id},
             "category": {"id": category_id}}
        ]}

        request = requests.post(url, data=json.dumps(myitem), headers=self.headers)
        if request.status_code == 200:
            return True

    def get_categories(self):
        url = self.base_url + 'categories' + self.api_token
        request = requests.get(url, headers=self.headers)
        if request.status_code == 200:
            return request.text

    def add_quantity(self, item_id, quantity):
        """Add quantity to item_id"""
        old_quantity = self.item_quantity(item_id)
        new_quantity = old_quantity + quantity
        url = self.base_url + 'item_stocks/' + item_id + self.api_token
        myitem = {'quantity': new_quantity}
        request = requests.post(url, data=json.dumps(myitem), headers=self.headers)

        if request.status_code == 200:
            return True

    def set_quantity(self, item_id, quantity):
        """Overwrite item_id's quantity with quantity, to add not overwrite use add_quantity()"""
        url = self.base_url + 'item_stocks/' + item_id + self.api_token
        myitem = {'quantity': quantity}
        request = requests.post(url, data=json.dumps(myitem), headers=self.headers)

        if request.status_code == 200:
            return True

    def item_quantity(self, item_id):
        """Return Current Item Quantity"""
        url = self.base_url + 'item_stocks/' + item_id + self.api_token
        request = requests.get(url)
        myreq = json.loads(request.text)
        try:
            quantity = myreq['quantity']
        except KeyError as err:
            quantity = 0
        if request.status_code == 200:
            return quantity


merchantId = 'xxxxxxx'
token = 'xxxxxx'
clover_client = CloverClient(merchantId, token)

# status, item_id = clover_client.add_item('tytytytytyt', 2454131, code=89934875)
# print(item_id)
# attach_category("PWMTWPXFVWBWY", "TS3APENXXQ94R")
