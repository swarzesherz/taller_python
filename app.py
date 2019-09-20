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
admin.add_view(CategoryModelView(Category, db.session, name=__('Categorias')))
admin.add_view(PostModelView(Post, db.session))
admin.add_view(UserModelView(User, db.session, name=__('Usuarios')))
admin.add_view(RoleModelView(Role, db.session, name=__('Roles')))


@app.cli.command("initdb")
def init_db():
    db.create_all()


@app.cli.command("create-post")
def create_post():
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
    post_category = Category(name='Python')
    Post(title='Hello Python!', body='Python is pretty cool',
         category=post_category)
    post = Post(title='Snakes', body='Ssssssss')
    post_category.posts.append(post)
    db.session.add(post_category)
    db.session.commit()


@app.route('/')
def hello_world():
    return 'Hello World!'


# https://flask.palletsprojects.com/en/1.1.x/quickstart/#http-methods
@app.route('/posts', methods=['GET'])
@login_required
def list_posts():
    categories = Category.query.options(joinedload('posts')).all()
    return render_template('posts.html', categories=categories)


if __name__ == '__main__':
    app.run()
