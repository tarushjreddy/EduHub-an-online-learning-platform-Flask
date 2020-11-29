from flask import Flask, render_template, Response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False,
                       default="Author not avialable")
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return "Blog post" + str(self.id)


all_posts = [
    {
        'title': 'this is the post number one',
        'author': 'Sunny Leone',
        'content': 'this is the content of the palce where it has post one'
    },
    {
        'title': 'this is the post number two',
        'content': 'this is the content of the palce where it has post two'
    }
]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/forms", methods=['GET', 'POST'])
def forms():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/forms')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('forms.html', posts=all_posts)


@app.route("/posts", methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    card = f"Sunnyleone is slut of {name}" + str(id)
    return card


@app.route('/offlline', methods=['GET'])
def getData():
    return "this is the get poster"


@app.route('/cars/<int:name>')
def car(name):
    card = "Sunnyleone is slut of" + str(name)
    return card


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':

        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        print("updated the data")
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('edit.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
