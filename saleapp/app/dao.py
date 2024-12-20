from app.models import Category, Product, User, Receipt, ReceiptDetails, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime


def load_categories():
    return Category.query.order_by('id').all()


def load_products(cate_id=None, kw=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()


def count_products():
    return Product.query.count()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username),
                          User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()


def add_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c


def revenue_stats():
    return db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
             .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)).group_by(Product.id).all()


def revenue_time(time='month', year=datetime.now().year):
    return db.session.query(func.extract(time, Receipt.created_date),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
        .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
        .filter(func.extract("year", Receipt.created_date).__eq__(year))\
        .group_by(func.extract(time, Receipt.created_date))\
        .order_by(-func.extract(time, Receipt.created_date)).all()


def count_products_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id).all()


def get_product_by_id(id):
    return Product.query.get(id)


def load_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).all()


if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())
