from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


posts = [{
    'author': 'Ranjan Kumar',
    'date_posted': '27-09-2000',
    'content': 'First post',
    'title': 'First post'
}, {
    'author': 'Shivam Kumar',
    'date_posted': '27-09-2000',
    'content': 'Second post',
    'title': 'Second post'
}]


@app.route('/')
@app.route('/home')
def home_handler():
    return render_template('home.html', title='Home Page')


@app.route('/about')
def about():
    return render_template('home.html', title='About')


@app.route('/posts')
def about_post():
    return render_template('posts.html', posts=posts)


@app.route('/auth/<type>')
def login(type):
    print(type)
    return 'Login Page'
