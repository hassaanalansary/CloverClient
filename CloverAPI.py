import json
import requests


class CloverClient(object):
    def __init__(self, merchant_id, auth_token):
        self.merchant_id = merchant_id
        self.auth_token = auth_token

        self.api_token = '?access_token=' + self.auth_token
        self.base_url = 'https://api.clover.com/v3/merchants/' + self.merchant_id + '/'
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def add_item(self, name: str, price: int, **kwargs):
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


merchantId = '76J5V198D5GRC'
token = 'e3c4d4e0-2f93-d603-9297-0b70b929868b'
clover_client = CloverClient(merchantId, token)
# status, item_id = clover_client.add_item('tytytytytyt', 2454131, code=89934875)
# print(item_id)
# attach_category("PWMTWPXFVWBWY", "TS3APENXXQ94R")
