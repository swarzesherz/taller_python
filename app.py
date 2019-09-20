from flask import Flask, render_template, request, session
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_babelex import Babel
from flask_babelex import lazy_gettext as __
from flask_security import MongoEngineUserDatastore, Security, login_required

from admin_views import (CategoryModelView, PostModelView, UserModelView,
                         RoleModelView)

app = Flask(__name__)
app.config.from_pyfile('config.py')
# Localización
babel = Babel(app)


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'es')


# MongoEngine
db = MongoEngine(app)

from models import (Post, Category, User, Role)  # NOQA

# Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Flask Admin
# https://bootswatch.com/3/
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
admin = Admin(app, name='Admin', template_mode='bootstrap3')

# Admin views
admin.add_view(CategoryModelView(Category, name=__('Categorias')))
admin.add_view(PostModelView(Post))
admin.add_view(UserModelView(User, name=__('Usuarios')))
admin.add_view(RoleModelView(Role, name=__('Roles')))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
