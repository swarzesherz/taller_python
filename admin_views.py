# https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views
from flask_admin.contrib.sqla import ModelView
from flask_babelex import lazy_gettext as __


class CategoryModelView(ModelView):
    can_delete = False
    column_labels = {
        'name': __('Nombre')
    }


class PostModelView(ModelView):
    form_excluded_columns = [
        'pub_date'
    ]
    column_labels = {
        'category': __('Categoria'),
        'title': __('Título'),
        'body': __('Mensaje'),
        'pub_date': __('Fecha de publicación')
    }

