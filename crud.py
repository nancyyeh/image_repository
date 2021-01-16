"""CRUD operations."""

from model import db, Image, ImageColor, Color, Inventory, connect_to_db


def create_image(title, url_path, uuid, width, height, file_size, date_added, status):
    """Create images"""
    if height == width:
        shape = "square"
    elif height > width:
        shape = "portrait"
    else:
        shape = "landscape"

    mp_size = round(((int(height) * int(width)) / 1000000), 2)

    image = Image(title=title, url_path=url_path, uuid=uuid, width=width,
                  height=height, file_size=file_size, date_added=date_added, status=status, shape=shape, mp_size=mp_size)
    db.session.add(image)
    db.session.commit()

    return image


def create_color(name):
    """Create color"""

    color = Color(name=name)
    db.session.add(color)
    db.session.commit()

    return color


def create_image_color(image_id, color_id):
    """creata a color and image connection."""

    image_color = ImageColor(
        image_id=image_id, color_id=color_id)
    db.session.add(image_color)
    db.session.commit()

    return image_color


def create_inventory(image_id, quantity, price):
    """create an inventory record"""

    image_inventory = Inventory(
        image_id=image_id, quantity=quantity, price=price)
    db.session.add(image_inventory)
    db.session.commit()

    return image_inventory


def update_inventory(image_id, quantity=None, price=None):

    image_inventory = Inventory.query.filter_by(image_id=image_id).first()
    if quantity is not None:
        image_inventory.quantity = quantity
    if price is not None:
        image_inventory.price = price
    db.session.commit()

    return image_inventory


# IMAGE SEARCH FUNCTIONALITY

def search_images(term, shapes, min_file_size, max_file_size, mp_size, colors):
    """return images based on search criteria"""

    query = Image.query

    if term:
        query = query.filter(Image.title.contains(term))

    if shapes:
        query = query.filter(Image.shape.in_(shapes))

    if min_file_size:
        query = query.filter(Image.file_size > min_file_size)
    if max_file_size:
        query = query.filter(Image.file_size < max_file_size)

    if mp_size:
        if mp_size == "small":
            query = query.filter(Image.mp_size < 12)
        if mp_size == "medium":
            query = query.filter(12 <= Image.mp_size,  Image.mp_size < 24)
        if mp_size == "large":
            query = query.filter(24 <= Image.mp_size)

    if colors:
        query = query.join(ImageColor).join(
            Color).filter(Color.name.in_(colors))

    return query.all()


# GET ALL


def get_all_images():
    "return all images"

    return Image.query.all()


def get_all_inventory():
    "return all inventory"

    return Inventory.query.all()


# GET BY IMAGE ID


def get_image_by_image_id(image_id):
    """Return a image by id."""

    return Image.query.get(image_id)


def get_inventory_by_image_id(image_id):
    """Return inventory information."""

    return Inventory.query.filter_by(image_id=image_id).first()


def get_color_by_image_id(image_id):
    """Return color code"""

    return ImageColor.query.filter_by(image_id=image_id).all()


# GET COLOR_ID BY COLOR

def get_id_by_color(name):
    """Return color id by color."""

    return Color.query.filter_by(name=name).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
