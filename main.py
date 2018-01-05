from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Longtext)

    def __init__(self, name):
        self.name = name


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog = request.form['new_post']
        blogs.append(blog)

    return render_template('blog_entries.html',title="Build A Blog", blogs=blogs)


if __name__ -- 'main':
    app.run()
