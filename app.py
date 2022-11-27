from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5433/products'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

# # untuk connect ke DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

app.secret_key = os.getenv('SECRETKEY')

# Create class Product untuk DB nya (extends db.model), define column + datatype
class Products(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  price = db.Column(db.Integer, nullable=False)
  description = db.Column(db.String, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  date_added = db.Column(db.DateTime, default=datetime.utcnow) # tetap butuh date untuk sort

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

# endpoint POST product
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
      db.session.commit() # untuk save ke databasenya
      return jsonify(message=f"Success adding {name} as a new product"), 201
    except Exception as e:
      print(e)
      return jsonify(message=f"Something went wrong! {e}")

@app.get("/products")
def fetch_products():
  products = Products.query.all()
  products_schema = ProductSchema(many=True)
  result = products_schema.dump(products)
  return jsonify(result), 200

if __name__ == "__main__":
  app.run(debug=True)