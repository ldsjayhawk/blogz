from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__ = 'Blogging'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():

    if request.method == 'GET':
        return render_template('blog_entries.html', title="Build A Blog", blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', title="Build A Blog")

    if request.method =='POST':
        blog_title = request.form['blog-title']
        blog = request.form['blog']
        #add error handling (is there a title? is there a blog post?)
        #create a blog object to put into database
        #add post to db and commit post to db
        return render_template('blog_entries.html', title="Build A Blog", blogs=blogs)

if __name__ == '__main__':
    app.run()
