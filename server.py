from app import app, db, User, Order, user_schema, users_schema, order_schema 
from app import orders_schema, Product, product_schema, products_schemas

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select


@app.route("/users", methods=["GET"])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_user = User(name=user_data['name'], email=user_data['email'], address=user_data['address'])
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    user.name = user_data["name"]
    user.email = user_data["email"]
    user.address = user_data["address"]
    db.session.commit()
    return user_schema.jsonify(user), 200


@app.route('/users/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid User ID"}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"Message": f"successfully deleted {user.name}"}), 200

#------------------------------------------------------------------------------------------------------
@app.route("/products", methods=["GET"])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()

    return products_schemas.jsonify(products), 200


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200


@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(product_name=product_data['product_name'], product_price=product_data['product_price'])
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201


@app.route("/products/<int:id>", methods=["PUT"])
def update_products(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    product.name = product_data["name"]
    product.price = product_data["price"]
    db.session.commit()
    return product_schema.jsonify(product), 200


@app.route('/products/<int:id>', methods=["DELETE"])
def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid Product ID"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"Message": f"successfully deleted {product.name}"}), 200

#------------------------------------------------------------------------------------------------------

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user_id = order_data['user_id']
    # product_ids = order_data['product_ids']
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    
    new_order = Order(order_date=order_data['order_date'], user_id=order_data['user_id'])
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201


@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['GET'])
def product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "invalid product id"}), 400
    
    if product in order.products:
        return jsonify({"message": "Product already in order"}), 400            
    order.products.append(product)
    db.session.commit()
    
    return order_schema.jsonify(order), 200



@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    if product not in order.products:
        return jsonify({"message": "Product not in order"}), 400
    
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"message": f"Successfully removed product {product_id} from order {order_id}"}), 200


@app.route('/orders/user/<int:user_id>', methods=['GET'])
def orders_for_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    orders = user.orders
    return orders_schema.jsonify(orders), 200


@app.route('/orders/<int:order_id>/products', methods=['GET'])
def products_for_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400

    products = order.products
    return products_schemas.jsonify(products), 200
# -------------------------------------------------------------------------------


if __name__ == '__main__':    
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
    