from flask import Blueprint, render_template, redirect, request, abort, url_for
from flask_login import login_required, current_user
from twitter import db
from twitter.models import Post
from twitter.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('post.html', title='New Post', form=form)


@posts.route('/post/<int:post_id>')
def current_post(post_id):
    post = Post.query.get(int(post_id))
    return render_template('current_post.html', title='Post',post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(int(post_id))
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('post.html', title='Update Post', post=post, form=form)

@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(int(post_id))
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home'))






