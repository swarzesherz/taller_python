# https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views
from flask_admin.contrib.sqla import ModelView


class CategoryModelView(ModelView):
    can_delete = False


class PostModelView(ModelView):
    form_excluded_columns = [
        'pub_date'
    ]

