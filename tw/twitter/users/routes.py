from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from twitter import db, bcrypt
from twitter.users.forms import RegistrationForm, LoginForm, UpdateProfileForm
from twitter.models import User, Post
from twitter.users.utils import crop_image

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        exists = bcrypt.check_password_hash(user.password, form.password.data)
        if user and exists:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful!')
    return render_template('login.html', title="Login", form=form)

@users.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = crop_image(form.picture.data)
            current_user.image_file = picture_name
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    return render_template('profile.html', title=f'{current_user.username}', posts=posts, form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))









