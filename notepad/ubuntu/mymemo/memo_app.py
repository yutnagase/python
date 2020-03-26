from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)


db_uri = 'mysql+pymysql://root:@localhost/memo?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())


@app.route('/')
def list():

    message = 'Hello paiza memo'
    posts = Post.query.all()

    return render_template('list.html', message = message, posts = posts)


@app.route('/show/<int:id>')
def show_post(id):

    message = 'Your memo ' + str(id)
    post = Post.query.get(id)

    return render_template('show.html', message = message, post = post)


@app.route('/new')
def new_post():

    message = 'New memo'
    return render_template('new.html', message = message)


@app.route('/create', methods=['POST'])
def create_post():

    message = 'create your memo'

    new_post = Post()
    new_post.title = request.form['title']
    new_post.content = request.form['content']
    db.session.add(new_post)
    db.session.commit()

    post = Post.query.get(new_post.id)

    return render_template('show.html', message = message, post = post)


@app.route('/destroy/<int:id>')
def destroy_post(id):

    message = 'Destroy your memo ' + str(id)

    destroy_post = Post.query.get(id)
    db.session.delete(destroy_post)
    db.session.commit()

    posts = Post.query.all()

    return render_template('list.html', message = message, posts = posts)


@app.route('/edit/<int:id>')
def edit_post(id):

    message = 'Edit your memo' + str(id)
    post = Post.query.get(id)
    
    return render_template('edit.html', message = message, post = post)
    


@app.route('/update/<int:id>', methods=['POST'])
def update_post(id):

    message = 'Update your memo' + str(id)

    post = Post.query.get(id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()

    return render_template('show.html', message = message, post = post)

