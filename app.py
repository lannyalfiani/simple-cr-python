from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # ORM
from datetime import datetime
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow # untuk convert python class instances ke object yg bisa jadi JSON
from sqlalchemy import desc
import os, redis, json

load_dotenv()

redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5433/products'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

# untuk connect ke DB
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.secret_key = os.getenv('SECRETKEY')
class Products(db.Model): # Create class Product untuk DB nya (extends db.model), define column + datatype
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  price = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  date_added = db.Column(db.DateTime, default=datetime.utcnow) # tetap butuh date untuk order by newest

  # constructor object (self = instance-nya)
  def __init__(self, name, price, description, quantity):
      self.name = name
      self.price = price
      self.description = description
      self.quantity = quantity
  
  def __repr__(self):
    return f"<Product {self.name}>"

# kalo ada ini, langsung create db.table di define ketika run servernya
with app.app_context():
  db.create_all()

class ProductSchema(ma.Schema):
  class Meta:
    fields = ("id", "name", "price", "description", "quantity", "date_added")

# ROUTES

# Untuk cek server berjalan atau tidak
@app.get("/")
def index():
  return {"message": "Hello World, server is up!"}

# POST product
@app.post("/products")
def add_product():
  if request.is_json:
    req = request.get_json()
    name = req.get("name")
    price = req.get("price")
    description = req.get("description")
    quantity = req.get("quantity")

    if not name or not price or not price or not description or not quantity:
      return jsonify(message="Please fill in all required fields!"), 400

    try:
      newProduct = Products(name, price, description, quantity)
      db.session.add(newProduct)
      db.session.commit() # to commit/save to DB

      redis_client.delete("newest_products")
      redis_client.delete("lowest_products")
      redis_client.delete("highest_products")
      redis_client.delete("a_z_products")
      redis_client.delete("z_a_products")

      return jsonify(message=f"Success adding {name} as a new product"), 201
    except Exception as e:
      print(e)
      return jsonify(message=f"Something went wrong! {e}")

#GET products endpointv
@app.get("/products")
def fetch_products():
  try:
    if request.args['query'] == 'date_added' and request.args['sort'] == 'newest':
      newest_products_cache = redis_client.get("newest_products")
      if newest_products_cache is None:
        products = Products.query.order_by(Products.date_added.desc()).all()
        product_schema = ProductSchema()
        products_schema = ProductSchema(many=True)
        result = products_schema.dump(products)
        redis_client.set("newest_products", json.dumps(result))
        return jsonify(result), 200
      else:
        return json.loads(newest_products_cache), 200


    elif request.args['query'] == 'price' and request.args['sort'] == 'highest':
      highest_products_cache = redis_client.get("highest_products")
      if highest_products_cache is None:
        products = Products.query.order_by(Products.price.desc()).all()
        product_schema = ProductSchema()
        products_schema = ProductSchema(many=True)
        result = products_schema.dump(products)
        redis_client.set("highest_products", json.dumps(result))
        return jsonify(result), 200
      else:
        return json.loads(highest_products_cache), 200

    elif request.args['query'] == 'price' and request.args['sort'] == 'lowest':
      lowest_products_cache = redis_client.get("lowest_products")
      if lowest_products_cache is None:
        products = Products.query.order_by(Products.price).all()
        product_schema = ProductSchema()
        products_schema = ProductSchema(many=True)
        result = products_schema.dump(products)
        redis_client.set("lowest_products", json.dumps(result))
        return jsonify(result), 200
      else:
        return json.loads(lowest_products_cache), 200


    elif request.args['query'] == 'name'and request.args['sort'] == 'a-z':
      a_z_cache = redis_client.get("a_z_products")

      if a_z_cache is None:
        products = Products.query.order_by(Products.name).all()
        product_schema = ProductSchema()
        products_schema = ProductSchema(many=True)
        result = products_schema.dump(products)
        redis_client.set("a_z_products", json.dumps(result))
        return jsonify(result), 200
      else:
        return json.loads(a_z_cache), 200

    elif request.args['query'] == 'name' and request.args['sort'] == 'z-a':
      z_a_cache = redis_client.get("z_a_products")

      if z_a_cache is None:
        products = Products.query.order_by(Products.name.desc()).all()
        product_schema = ProductSchema()
        products_schema = ProductSchema(many=True)
        result = products_schema.dump(products)
        redis_client.set("z_a_products", json.dumps(result))
        return jsonify(result), 200
      else:
        return json.loads(z_a_cache), 200

    else:
      return jsonify(message='Bad request, query string is not recognised!'), 400
  except Exception as error:
    return jsonify(message=f"Something went wrong! {error}"), 500

if __name__ == "__main__":
  app.run(debug=True)