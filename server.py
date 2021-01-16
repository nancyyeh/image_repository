"""Server for image repo."""

from flask import (Flask, render_template, request,
                   flash, session, redirect, jsonify)
from model import connect_to_db
import model
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/api/search', methods=['POST'])
def search_images():
    """create a image search"""
    term = request.json.get("term")
    shapes = request.json.get("shapes")
    min_file_size = request.json.get("min_file_size")
    max_file_size = request.json.get("max_file_size")
    # large 24MP (24+), medium 12MP (12-24), small 4MP (4-12)
    mp_size = request.json.get("mp_size")
    colors = request.json.get("colors")

    search = crud.search_images(
        term, shapes, min_file_size, max_file_size, mp_size, colors)

    lst_images = []

    for image in search:
        lst_images.append(image.todict())

    return jsonify(lst_images)


@app.route('/api/images/<image_id>', methods=['GET'])
def image_details(image_id):

    image = crud.get_image_by_image_id(image_id)

    return jsonify(image.todict())


@app.route('/api/images', methods=['GET'])
def all_images():

    images = crud.get_all_images()

    lst_images = []

    for image in images:
        lst_images.append(image.todict())

    return jsonify(lst_images)


# Invenory management APIs

@app.route('/api/inventory/<image_id>', methods=['GET'])
def return_inventory(image_id):
    """return json file of just one image's inventory information"""

    inventory = crud.get_inventory_by_image_id(image_id)

    if inventory:
        return jsonify(inventory.todict())
    else:
        return jsonify({
            "message": 'There is no inventory for the image.'
        }), 400


@app.route('/api/inventory/<image_id>', methods=['POST'])
def create_inventory(image_id):

    quantity = request.json.get("quantity")
    if type(quantity) != int:
        return jsonify({
            "message": 'Invalid quantity input.'
        }), 400

    # Price is in cents, front-end will handle the conversion from cent to dollar to avoid float end problems
    price = request.json.get("price")
    if type(price) != int:
        return jsonify({
            "message": 'Invalid price input.'
        }), 400

    if crud.get_inventory_by_image_id(image_id):
        return jsonify({
            "message": 'Inventory record for the image exist, to update please use the update API.'
        }), 400

    image_inventory = crud.create_inventory(image_id, quantity, price)

    return jsonify(image_inventory.todict())


@app.route('/api/inventory/<image_id>', methods=['PATCH'])
def update_inventory(image_id):
    "input image id and data to update the inventory information"

    quantity = request.json.get("quantity")
    if type(quantity) != int:
        return jsonify({
            "message": 'Invalid quantity input.'
        }), 400

    # Price is in cents, front-end will handle the conversion from cent to dollar to avoid float end problems
    price = request.json.get("price")
    if type(price) != int:
        return jsonify({
            "message": 'Invalid price input.'
        }), 400

    image_inventory = crud.update_inventory(image_id, quantity, price)

    return jsonify(image_inventory.todict())


@app.route('/api/inventories', methods=['GET'])
def return_all_inventory():
    """return json file of a list of images with it's inventory information"""

    inventories = crud.get_all_inventory()

    lst_inventories = []

    for inventory in inventories:
        lst_inventories.append(inventory.todict())

    return jsonify(lst_inventories)


# e-commerence APIs

@app.route('/api/inventory/sell/<image_id>', methods=['POST'])
def sold_image(image_id):
    "sell image, input: image_id and quantity sold, update inventory and return updated inventory"

    try:
        quantity_sold = int(request.json.get("quantity_sold"))
    except:
        return jsonify({
            "message": 'Invalid quantity sold input.'
        }), 400

    image_inventory = crud.get_inventory_by_image_id(image_id)

    if image_inventory.quantity < quantity_sold:
        return jsonify({
            "message": 'Not enough stock.'
        }), 400
    else:
        remaining_quantity = image_inventory.quantity - quantity_sold
        new_inventory = crud.update_inventory(image_id, remaining_quantity)

    return jsonify(new_inventory.todict())


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
