from typing import TypedDict
from flask import Flask, jsonify, request


class StoreItems(TypedDict, total=True):
    name: str
    price: float


class Store(TypedDict, total=False):
    name: str
    items: list[StoreItems]


app = Flask(__name__)

stores = [
    {
        'name': 'My wonderful store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]


@app.route(rule='/stores', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = Store()
    store_name = request_data.get('name', None)
    new_store['name'] = store_name.title()
    new_store['items'] = []
    stores.append(new_store)
    return jsonify(new_store)


@app.route(rule='/stores/<string:name>', methods=['GET'])
def get_store(name: str):
    for store in stores:
        if store['name'] == name.title():
            return jsonify(store)
    return jsonify({'message': 'store not found'}), 400


@app.route(rule='/stores', methods=['GET'])
def get_stores():
    return jsonify(stores)


@app.route(rule='/stores/<string:name>/items', methods=['POST'])
def create_store_item(name: str):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name.title():
            for item in request_data:
                items = StoreItems()
                item_name = item.get('name', None)
                item_price = item.get('price', 0.00)
                items['name'] = item_name.title()
                items['price'] = item_price
                store['items'].append(items)
            return jsonify(store['items'])
    return jsonify({'message': 'store not found'}), 400


@app.route(rule='/stores/<string:name>/items', methods=['GET'])
def get_store_items(name: str):
    for store in stores:
        if store['name'] == name.title():
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'}), 400
