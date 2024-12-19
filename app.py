# py -m venv venv | python3 -m venv venv - create virtual env
# venv\Scripts\activate | source venv/bin/activate - activate virtual env 
# pip install Flask Flask-SQLAlchemy Flask-Marshmallow mysql-connector-python marshmallow-sqlalchemy
# pip freeze > requirements.txt - Saving list of installed packages

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey, Table, String, Column, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:!Howell4955@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)


order_products = Table(
    "order_products",
    Base.metadata,
    Column("order_id", ForeignKey("orders.order_id")),
    Column("product_id", ForeignKey("products.product_id")),   
)

user_orders = Table(
	"user_orders",
	Base.metadata,
	Column("user_id", ForeignKey("users.user_id")),
	Column("order_id", ForeignKey("orders.order_id")),
)


# User model
class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), unique=True)    
    orders: Mapped[List["Order"]] = relationship(secondary=user_orders, back_populates="users")



class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[DateTime] = mapped_column(DateTime, default=DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    users: Mapped[List["User"]] = relationship(secondary=user_orders, back_populates="orders")
    products: Mapped[List["Product"]] = relationship(secondary=order_products, back_populates="orders")


class Product(Base):
    __tablename__ = "products"
    
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(30))
    product_price: Mapped[int] = mapped_column()
    orders: Mapped[List["Order"]] = relationship(secondary=order_products, back_populates="products")



# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
# Order Schema
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        
# Product Schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
       
       
# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True) #Can serialize many User objects (a list of them)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schemas = ProductSchema(many=True)