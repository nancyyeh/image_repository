"""Models for image repo."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Image(db.Model):
    """Image"""

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    title = db.Column(db.String, nullable=False)
    url_path = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False)
    shape = db.Column(db.String, nullable=False)
    mp_size = db.Column(db.Integer, nullable=False)

    def todict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url_path": self.url_path,
            "uuid": self.uuid,
            "width": self.width,
            "height": self.height,
            "file_size": self.file_size,
            "date_added": self.date_added,
            "status": self.status,
            "shape": self.shape,
            "mp_size": self.mp_size,
        }

    def __repr__(self):
        return f'<Image image_id={self.id} uuid={self.uuid} title={self.title} url={self.url_path} width={self.width} height={self.height} file_size={self.file_size} date_added={self.date_added} status={self.status}>'


class ImageColor(db.Model):

    __tablename__ = "image_color"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    color_id = db.Column(
        db.Integer, db.ForeignKey('colors.id'))

    image = db.relationship('Image', backref='image_color')
    color = db.relationship('Color', backref='image_color')

    def __repr__(self):
        return f'<Image Tag id={self.id} image_id={self.image_id} tag_id={self.tag_id} >'


class Color(db.Model):

    __tablename__ = "colors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    name = db.Column(db.String, nullable=False)


class Inventory(db.Model):
    """Inventory"""

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # price is in cents

    def todict(self):
        return {
            "id": self.id,
            "image_id": self.image_id,
            "quantity": self.quantity,
            "price": self.price,
        }

    def __repr__(self):
        return f'<Inventory inventory_id={self.id} image_id={self.image_id} quantity={self.quantity} price={self.price}>'


class Discount(db.Model):
    """Discount"""

    __tablename__ = 'discount'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    discount = db.Column(db.Integer)
    discount_start_date = db.Column(db.DateTime)
    discount_end_date = db.Column(db.DateTime)


def connect_to_db(flask_app, db_uri='postgresql:///image_repo', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
