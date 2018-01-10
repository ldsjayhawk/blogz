from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    #ownerid = db.Column(db.String())

    def __init__(self, title, body, ownerid):
        self.title = title
        self.body = body
        #self.ownerid = ownerid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    #blogs = db.Column(db.String())

    def __init__(self, username, password, blogs):
        self.username = username
        self.password = password
        #self.blogs = blogs

@app.before_request
def require_login():
    if 'email' not in session:
        return redirect('/login')
    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user - User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            return redirect('/')
        else:
            #why did user fail to login
            return "<h3>Error!</h3>" #redirect('/login')

    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form('email')
        password = request.form('password')
        verify = request.form('verify')
        #Validate
        
        existing_user - User.query.filter_by(email=email).first()
        if not existing_user():
            new_user = User(email,password)
            db.session.add(new_user)
            db.session_commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h3>Duplicate User</h3>"
        
    return render_template('register.html', title="Register")

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        blogs = Blog.query.all()
        return render_template('blog_entries.html', title="Blogz", blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', title="Add New Post")

    if request.method =='POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog_post']
        blank_blog_title_error = ""
        blank_blog_error = ""

        if blog_title == "":
            blank_blog_title_error = "Blog title cannot be blank."

        if blog_post == "":
            blank_blog_error = "Blog post cannot be blank."

        new_blog = Blog(blog_title, blog_post)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()

        if blank_blog_title_error != "" or blank_blog_error != "":
            return render_template('new_post.html', title="Blogz", blogs=blogs, 
            blank_blog_title_error=blank_blog_title_error, blank_blog_error=blank_blog_error)
            

        else: 
            return render_template('blog_entries.html', title="Add", blogs=blogs)

@app.route('/blog', methods=['GET'])
def single_post():
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        return render_template('single_post.html', title="Blogz", blog=blog)


if __name__ == '__main__':
    app.run()