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
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        blogs = Blog.query.all()
        return render_template('blog_entries.html', title="Build A Blog", blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', title="Add New Post")

    if request.method =='POST':
        blog_title = request.form['blog-title']
        blog = request.form['blog']
        blank_blog_title_error = ""
        blank_blog_error = ""

        if " " in blog_title:
            blank_blog_title_error = "Blog title cannot be blank."

        if " " in blog:
            blank_blog_error = "Blog post cannot be blank."

        new_blog = Blog(blog_title, blog)
        db.session.add(new_blog)
        db.session.commit
        blogs = Blog.query.all()
        return render_template('blog_entries.html', title="Build A Blog", blogs=blogs, 
            blank_blog_title_error=blank_blog_title_error, blank_blog_error=blank_blog_error)

@app.route('/singlepost', methods=['POST','GET'])
def single_post():
    if request.method == 'GET':
        blog_id = int(request.args.get['blog-id'])
        blog = Task.query.get(task_id)        
        return render_template('single_post.html', title="Build A Blog", blog_id=blog_id, blog=blog)


if __name__ == '__main__':
    app.run()
