# https://flask-admin.readthedocs.io/en/latest/introduction/#customizing-built-in-views
from flask import abort, redirect, url_for, request
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import SecureForm
from flask_babelex import lazy_gettext as __
from flask_security import current_user
import flask_security.utils as security_utils


class SecureModelView(ModelView):
    form_base_class = SecureForm

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('admin')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class CategoryModelView(SecureModelView):
    can_delete = False
    column_labels = {
        'name': __('Nombre')
    }


class PostModelView(SecureModelView):
    form_excluded_columns = [
        'pub_date'
    ]
    column_labels = {
        'category': __('Categoria'),
        'title': __('Título'),
        'body': __('Mensaje'),
        'pub_date': __('Fecha de publicación')
    }


class RoleModelView(SecureModelView):
    pass


class UserModelView(SecureModelView):
    def on_model_change(self, form, model, is_created):
        model.password = security_utils.hash_password(model.password)

