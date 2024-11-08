from app.models import Category, Product


def load_categories():
    return Category.query.order_by('id').all()


def load_products(cate_id=None, kw=None):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    return query.all()
