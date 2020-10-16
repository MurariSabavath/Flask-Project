from flask import Blueprint, render_template
from twitter.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', title = "Home", posts = posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About')