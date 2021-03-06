from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'zxcvbnmmasdfghjkl'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:
            flash('Invalid Login', 'error')
            return redirect('/register.html')
    
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify-password']
        existing_user = User.query.filter_by(username=username).first()
        
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            username_error = "This username already exists"
            return render_template('login.html', username=username, username_error=username_error) 
        
    return render_template('register.html', title="Register")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

@app.route('/', methods=['GET'])
def user_index():
    if request.method == 'GET':
        users = User.query.all()
    return render_template('index.html', title="Blogz", users=users)

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', title="Add New Post")

    if request.method =='POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        blank_blog_title_error = ""
        blank_blog_error = ""

        if blog_title == "":
            flash('Blog title cannot be blank.', 'error')
            #blank_blog_title_error = "Blog title cannot be blank."

        if blog_post == "":
            flash('Blog post cannot be blank.', 'error')
            #blank_blog_error = "Blog post cannot be blank."

        if blank_blog_title_error != "" or blank_blog_error != "":
            return render_template('new_post.html', title="Blogz", blogs=blogs, 
            blank_blog_title_error=blank_blog_title_error, blank_blog_error=blank_blog_error)
             
        
        user = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, blog_post, user)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()
        query_param_url = "/blog?id=" + str(new_blog.id)
        return redirect(query_param_url)
        #return redirect('/blog?user=user.id')
        #return render_template('blog_entries.html', title="Add", blogs=blogs)

@app.route('/index', methods=['GET'])
def index():
    if request.args:
        user_id = request.args.get("user")
        user=User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=user).all()
        return render_template('user_blogs.html', title="Blogz", blogs=blogs) 

@app.route('/blog', methods=['GET'])
def single_post():
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        return render_template('single_post.html', title="Blogz", blog=blog)


if __name__ == '__main__':
    app.run()