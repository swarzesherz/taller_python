# https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views
from flask_admin.contrib.sqla import ModelView
from flask_babelex import lazy_gettext as __
import flask_security.utils as security_utils


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


class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.password = security_utils.hash_password(model.password)

