from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

blogs = []

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
        blogs.append(blog)
        #add error handling (is there a title? is there a blog post?)
        #create a blog object to put into database
        #add post to db and commit post to db
        return render_template('blog_entries.html', title="Build A Blog", blogs=blogs)

#if__name__ == 'main':
app.run()
