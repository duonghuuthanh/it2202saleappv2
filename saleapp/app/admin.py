from app.models import Category, Product, User, UserRole, Receipt, ReceiptDetails
from app import app, db, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())


admin = Admin(app=app, name='eCommerce Admin', template_mode='bootstrap4', index_view=MyAdminIndexView())


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class CategoryView(AdminView):
    column_list = ['name', 'products']


class ProductView(AdminView):
    column_list = ['id', 'name', 'price', 'active']
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    page_size = 10
    column_editable_list = ['name']


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',
                           stats=dao.revenue_stats(), stats2=dao.revenue_time())


admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Receipt, db.session))
admin.add_view(AdminView(ReceiptDetails, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
