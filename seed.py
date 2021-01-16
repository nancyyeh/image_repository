import os
import json
from random import choice, randint
from datetime import datetime
import uuid

import crud
import model
import server

os.system('dropdb image_repo')
os.system('createdb image_repo')

model.connect_to_db(server.app)
model.db.create_all()


# BELOW SCRIPT TO CREATE DUMMY DATA

# Dummy color data
list_colors = ['white', 'black', 'yellow', 'orange',
               'pink', 'red', 'purple', 'blue', 'green', 'brown', ]

# Create colors
for color in list_colors:
    crud.create_color(color)

# Load dummy images data from JSON file
with open('data/images.json') as f:
    image_data = json.loads(f.read())

# Create images
for image in image_data:
    # create the images
    title, url_path = (image['title'], image['url_path'])
    uuid_num = uuid.uuid4()
    width, height = (image['width'], image['height'])
    file_size = image['file_size']
    date_added = datetime.strptime(image['date_added'], '%Y-%m-%d')
    status = image['status']

    image_obj = crud.create_image(title,
                                  url_path,
                                  uuid_num,
                                  width,
                                  height,
                                  file_size,
                                  date_added,
                                  status)

    # link to the colors
    colors = image['colors']
    for color in colors:
        color_obj = crud.get_id_by_color(color)
        crud.create_image_color(image_obj.id, color_obj.id)
