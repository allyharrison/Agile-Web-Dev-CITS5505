from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from urllib.parse import urlsplit
from app.forms import EmptyForm
from flask_login import logout_user


@app.route("/")
def html():
    return render_template("HTML.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("html"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("html")
        return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("html"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("html"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


from datetime import datetime, timezone


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)
# Keep this for rendering
from app.forms import PostForm
from app.models import Post


@app.route('/', methods=['GET', 'POST'])
@app.route('/blog', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('blog'))
    posts = db.session.scalars(current_user.following_posts()).all()
    return render_template("blog.html", title='Home Page', form=form,
                           posts=posts)
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template("blog.html", title='Explore', posts=posts.items)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('html'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('html'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('html'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('html'))

# Below is older stiff can be turned into html tag 
@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/new_restaurants")
def new_restaurants():
    return render_template("new_restaurants.html")


@app.route("/cuisine")
def cuisine():
    return render_template("cuisine.html")


@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/blog")
def blog():

    return render_template("blog.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = Post()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("blog"))
    return render_template("create.html", title="Create Post", form=form)


@app.route("/<int:id>/edit/", methods=("GET", "POST"))
def edit(id):
    # post = get_post(id)
    return render_template("edit.html")


@app.route("/<int:id>/delete/", methods=("POST",))
def delete(id):

    return redirect(url_for("blog"))
