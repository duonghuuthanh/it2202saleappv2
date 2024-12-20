from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.username


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

    def __str__(self):
        return self.id


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # u = User(name='admin', username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()
        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        # c3 = Category(name='Laptop')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        #
        # products = [{
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1691062682/tkeflqgroeil781yplxt.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Galaxy Note 10 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Galaxy Tab S9",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1691062682/tkeflqgroeil781yplxt.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Galaxy Note 10 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Galaxy Tab S9",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1691062682/tkeflqgroeil781yplxt.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Galaxy Note 10 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Galaxy Tab S9",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1691062682/tkeflqgroeil781yplxt.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Galaxy Note 10 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1690011099/uobyqhus0bhqt1qbh1qp.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Galaxy Tab S9",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image": "https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg",
        #     "category_id": 2
        # }]
        #
        # for p in products:
        #     prod = Product(**p)
        #     db.session.add(prod)
        #
        # db.session.commit()

        c1 = Comment(content='good', user_id=1, product_id=1)
        c2 = Comment(content='nice', user_id=1, product_id=1)
        c3 = Comment(content='excellent', user_id=1, product_id=1)

        db.session.add_all([c1, c2, c3])
        db.session.commit()
