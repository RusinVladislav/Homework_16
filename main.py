from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from data_file import USERS_FILE, ORDERS_FILE, OFFERS_FILE
from utils import load_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(300))
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order')
    executor_id = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order')
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    offer = db.relationship('Offer')


db.drop_all()
db.create_all()

# заполняем таблицу User данными
users = load_data(USERS_FILE)
for user in users:
    user = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    )
    db.session.add(user)
    db.session.commit()

# заполняем таблицу Order данными
orders = load_data(ORDERS_FILE)
for order in orders:
    order = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )
    db.session.add(order)
    db.session.commit()

# заполняем таблицу Offer данными
offers = load_data(OFFERS_FILE)
for offer in offers:
    offer = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'],
    )
    db.session.add(offer)
    db.session.commit()

# роут для users с методами GET и POST
@app.route("/users/", methods=["GET", "POST"])
def get_all_users():
    """
    :return: all users in list(dict)
    """

    if request.method == "GET":
        all_users = User.query.all()
        result = []
        for user in all_users:
            result.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            })
        return jsonify(result)
    elif request.method == "POST":
        user_data = request.json
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return f"New user with name: {new_user.first_name} add"


# роут для users с методами GET и PUT и DELETE
@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user_manager(uid):
    """
    :return: one user for id in list(dict)
             PUT user by id
             DELETE user by id
    """

    user = User.query.get(uid)
    if request.method == "GET":
        if user is None:
            return "User not found"

        result = []
        result.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        })
        return jsonify(result)
    elif request.method == "PUT":
        user_data = request.json
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        return f'Update data user id: {uid}'

    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return f'User with id {uid} DELETE'


# роут для orders с методами GET и POST
@app.route("/orders/", methods=["GET", "POST"])
def get_all_orders():
    """
    :return: all orders in list(dict)
    """

    if request.method == "GET":
        all_orders = Order.query.all()
        result = []
        for order in all_orders:
            result.append({
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'price': order.price,
                'customer_id': order.customer_id,
                'executor_id': order.executor_id
            })
        return jsonify(result)
    elif request.method == "POST":
        order_data = request.json
        new_order = Order(**order_data)
        db.session.add(new_order)
        db.session.commit()
        return f"New order with name: {new_order.name} add"


# роут для orders с методами GET и PUT и DELETE
@app.route("/orders/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order_manager(uid):
    """
    :return: GET one order for id in list(dict)
             PUT order by id
             DELETE order by id
    """

    order = Order.query.get(uid)
    if request.method == "GET":
        if order is None:
            return "Order not found"

        result = []
        result.append({
            'id': order.id,
            'name': order.name,
            'description': order.description,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'price': order.price,
            'customer_id': order.customer_id,
            'executor_id': order.executor_id
        })
        return jsonify(result)
    elif request.method == "PUT":
        order_data = request.json
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = order_data['start_date']
        order.end_date = order_data['end_date']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        return f'Update data order id: {uid}'

    elif request.method == "DELETE":
        db.session.delete(order)
        db.session.commit()
        return f'Order with id {uid} DELETE'


# роут для offers с методами GET и POST
@app.route("/offers/", methods=["GET", "POST"])
def get_all_offers():
    """
    :return: all offers in list(dict)
    """

    if request.method == "GET":
        all_offers = Offer.query.all()
        result = []
        for offer in all_offers:
            result.append({
                'id': offer.id,
                'order_id': offer.order_id,
                'executor_id': offer.executor_id
            })
        return jsonify(result)
    elif request.method == "POST":
        offer_data = request.json
        new_offer = Offer(**offer_data)
        db.session.add(new_offer)
        db.session.commit()
        return f"New offer with order_id: {new_offer.order_id} add"


# роут для offers с методами GET и PUT и DELETE
@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer_manager(uid):
    """
    :return: GET one offer for id in list(dict)
             PUT offer by id
             DELETE offer by id
    """

    offer = Offer.query.get(uid)

    if request.method == "GET":
        if offer is None:
            return "Offer not found"
        result = []
        result.append({
            'id': offer.id,
            'order_id': offer.order_id,
            'executor_id': offer.executor_id
        })
        return jsonify(result)
    elif request.method == "PUT":
        offer_data = request.json
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return f'Update data offer id: {uid}'
    elif request.method == "DELETE":
        db.session.delete(offer)
        db.session.commit()
        return f'Offer with id {uid} DELETE'


if __name__ == '__main__':
    app.run()
