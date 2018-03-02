import json
import pypyodbc
import requests

myres = requests.get(
    # "https://api.clover.com/v3/merchants/76J5V198D5GRC/items?access_token=e3c4d4e0-2f93-d603-9297-0b70b929868b").text
    "https://api.clover.com/v3/merchants/76J5V198D5GRC/items/PWMTWPXFVWBWY/categories?access_token=e3c4d4e0-2f93-d603-9297-0b70b929868b").text

print(myres)
x = json.loads(myres)
# print(json.dumps(x, indent=4, sort_keys=True))
# print(x)
for i in x['elements']:
    ""
    # print(x)

db_file = "C:\\SproutFittersBE\\Sproutfitters Inventory BE1.7.2.accdb"
db_user, db_password = '', ''
db_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;UID=%s;PWD=%s' % (db_file, db_user, db_password)
conn = pypyodbc.connect(db_conn_str)
cursor = conn.cursor()
sql = "SELECT * FROM Items"
cursor.execute(sql)
db_items = cursor.fetchall()
for item in db_items:
    pass
    # print(item)

myitem = {'name': 'pytest2', 'price': 5646, 'code': '11100', 'sku': 'qwert'}

merchantId = '76J5V198D5GRC'
token = 'e3c4d4e0-2f93-d603-9297-0b70b929868b'
apiToken = '?access_token=' + token
baseURL = 'https://api.clover.com/v3/merchants/' + merchantId + '/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}




def add_item(name: str, price: int, **kwargs):
    if len(name)> 127: # clover doesnt accept more than 127 characters
        name = name[:127]
    myitem = {'name': name, 'price': price}
    for key in kwargs.keys():
        value = kwargs[key]
        myitem[key] = value

    url = baseURL + 'items' + apiToken
    request = requests.post(url, data=json.dumps(myitem), headers=headers)

    if request.status_code == 200:
        text = json.loads(request.text)
        return [True, text['id']]
    else:
        return [False, request.text]


# status, item_id = add_item('dunctest', 2131, code=89934875)
# print(item_id)

def attach_category(item_id, category_id):
    url = baseURL + 'category_items' + apiToken
    myitem = {'elements': [
        {"item": {"id": item_id},
         "category": {"id": category_id}}
    ]}
    request = requests.post(url, data=json.dumps(myitem), headers=headers)
    if request.status_code == 200:
        return True


attach_category("PWMTWPXFVWBWY", "TS3APENXXQ94R")
