from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post, Comment
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from urllib.parse import urlsplit
from app.forms import EmptyForm
from flask_login import logout_user
from flask_babel import _
from flask import g
from flask_babel import get_locale
from langdetect import detect, LangDetectException
from app.translate import translate
from langdetect import detect_langs
from app.forms import MessageForm
from app.models import Message
from app.forms import PostForm
from app.forms import CommentForm
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import sqlalchemy.orm as so
import os


# Route for the homepage
@app.route("/")
def html():
    return render_template("HTML.html")


# Route for logging in
@app.route("/login", methods=["GET", "POST"]) # Adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
def login():
    if current_user.is_authenticated:
        return redirect(url_for("html"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", category="danger")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("html")
        return redirect(next_page)
    return render_template("login.html", form=form)


# Route for logging out
@app.route("/logout") # used from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
def logout():
    logout_user()
    return redirect(url_for("html"))


# Route for user registration
@app.route("/register", methods=["GET", "POST"]) # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
def register():
    if current_user.is_authenticated:
        return redirect(url_for("html"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # login_user(user)
        flash("Congratulations, you are now a registered user!", category="success")
        # return redirect(url_for("html"))
    return render_template("register.html", title="Register", form=form)


# Route to view a user's profile
@app.route('/user/<username>') # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)

    query = user.posts.select().order_by(Post.timestamp.desc())

    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'],
                        error_out=False)
    
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
   
   
    comments = {post.id: Comment.query.filter_by(post_id=post.id).options(so.joinedload(Comment.user)).order_by(Comment.date_posted.desc()).all() for post in posts.items}
 
    form = EmptyForm()
    comment_form = CommentForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form, comment_form=comment_form, comments=comments)


# Hook to run before each request
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
        g.locale = str(get_locale())


# Route to edit user profile
@app.route("/edit_profile", methods=["GET", "POST"]) # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            # Save the uploaded image
            filename = secure_filename(form.profile_image.data.filename)
            form.profile_image.data.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )
            current_user.profile_image = filename
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.", category="success")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


# Route for the main index page
@app.route("/", methods=["GET", "POST"]) # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@app.route("/blog", methods=["GET", "POST"])
@login_required
def index():
    post_form = PostForm()
    comment_form = CommentForm()

    # Handle post submission
    if post_form.validate_on_submit() and "post" in request.form:
        try:
            possible_langs = detect_langs(post_form.post.data)
            most_probable_lang = max(possible_langs, key=lambda x: x.prob)
            if most_probable_lang.prob > 0.9:
                language = most_probable_lang.lang
            else:
                language = ""
        except LangDetectException:
            language = ""
        post = Post(body=post_form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()

        flash(_("Your post is now live!"), category="success")
        return redirect(url_for("blog"))
    # Handle comment submission
    if comment_form.validate_on_submit() and "comment" in request.form:
        post_id = request.form.get("post_id")
        post = Post.query.get_or_404(post_id)
        comment = Comment(
            content=comment_form.content.data, post_id=post.id, user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash(_("Your comment has been posted!"), category="success")
        return redirect(url_for("index"))

    # Fetch posts and their comments
    page = request.args.get("page", 1, type=int)
    posts = db.paginate(
        current_user.following_posts(),
        page=page,
        per_page=app.config["POSTS_PER_PAGE"],
        error_out=False,
    )
    next_url = url_for("index", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("index", page=posts.prev_num) if posts.has_prev else None

    # Fetch comments with their users for each post
    comments = {
        post.id: db.session.query(Comment)
        .filter_by(post_id=post.id)
        .options(so.joinedload(Comment.user))
        .order_by(Comment.date_posted.desc())
        .all()
        for post in posts.items
    }

    return render_template(
        "blog.html",
        title="Home",
        form=post_form,
        comment_form=comment_form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
        comments=comments,
    )


# Route to handle comment submission
@app.route("/comment", methods=["POST"])
@login_required
def comment():
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        post_id = request.form.get("post_id")
        post = Post.query.get_or_404(post_id)
        comment = Comment(
            content=comment_form.content.data, post_id=post.id, user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash(_("Your comment has been posted!"), category="success")
    return redirect(url_for("blog"))


# Route to explore posts made
@app.route("/explore") # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(
        query, page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False
    )
    next_url = url_for("explore", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("explore", page=posts.prev_num) if posts.has_prev else None

    comment_form = CommentForm()

    # Fetch comments with their users for each post
    comments = {
        post.id: db.session.query(Comment)
        .filter_by(post_id=post.id)
        .options(so.joinedload(Comment.user))
        .order_by(Comment.date_posted.desc())
        .all()
        for post in posts.items
    }

    return render_template(
        "blog.html",
        title="Explore",
        form=None,
        comment_form=comment_form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
        comments=comments,
    )


# Route to follow user
@app.route("/follow/<username>", methods=["POST"]) # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(
                _("User %(username)s not found.", username=username), category="danger"
            )
            return redirect(url_for("html"))
        if user == current_user:
            flash("You cannot follow yourself!")
            return redirect(url_for("user", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f"You are following {username}!", category="success")
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("html"))


# Route to unfollow a user
@app.route("/unfollow/<username>", methods=["POST"]) # adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(f"User {username} not found.")
            return redirect(url_for("html"))
        if user == current_user:
            flash("You cannot unfollow yourself!")
            return redirect(url_for("user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"You are not following {username}.")
        return redirect(url_for("user", username=username))
    else:
        return redirect(url_for("html"))


@app.route("/recipes")
def recipes():
    recipe_type = request.args.get(
        "type", "default"
    )  # Get the 'type' query parameter, default to 'default' if not present
    if recipe_type == "breakfast":
        title = "Breakfast Recipes"
    elif recipe_type == "lunch":
        title = "Lunch Recipes"
    elif recipe_type == "dinner":
        title = "Dinner Recipes"
    else:
        title = "Recipes"  # General title

    return render_template("recipes.html", title=title, type=recipe_type)


@app.route("/new_restaurants")
def new_restaurants():
    return render_template("new_restaurants.html", title="New Restaurants")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/hidden_gems")
def hidden_gems():
    return render_template("hidden_gems.html")


# Route to post
@app.route("/create", methods=["GET", "POST"]) #adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
@login_required
def create():
    form = Post()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", category="success")
        return redirect(url_for("blog"))
    return render_template("create.html", title="Create Post", form=form)


@app.route("/translate", methods=["POST"])
@login_required
def translate_text():
    data = request.get_json()
    return {
        "text": translate(data["text"], data["source_language"], data["dest_language"])
    }


@app.route("/search")
@login_required
def search():
    query = request.args.get("query", "", type=str)
    if not query:
        return redirect("/")  # Redirect if the query is empty

    print(f"Search query: {query}")  # Debug print

    page = request.args.get("page", 1, type=int)
    posts, total = Post.search(query, page, app.config["POSTS_PER_PAGE"])

    posts_list = list(posts)  # Convert ScalarResult to list
    print(f"Total results: {total}")  # Debug print

    next_url = (
        url_for("search", query=query, page=page + 1)
        if total > page * app.config["POSTS_PER_PAGE"]
        else None
    )
    prev_url = url_for("search", query=query, page=page - 1) if page > 1 else None

    comment_form = CommentForm()
    comments = {
        post.id: db.session.query(Comment)
        .filter_by(post_id=post.id)
        .options(so.joinedload(Comment.user))
        .order_by(Comment.date_posted.desc())
        .all()
        for post in posts_list
    }

    # Debug print the context being passed to the template
    print(f"Posts: {posts_list}, Comments: {comments}, Query: {query}")

    return render_template(
        "search.html",
        title="Search",
        posts=posts_list,
        next_url=next_url,
        prev_url=prev_url,
        query=query,
        comment_form=comment_form,
        comments=comments,
    )


@app.route("/send_message/<recipient>", methods=["GET", "POST"])
@login_required
def send_message(recipient):
    user = db.first_or_404(sa.select(User).where(User.username == recipient))
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(_("Your message has been sent.", category="success"))
        return redirect(url_for("user", username=recipient))
    return render_template(
        "send_message.html", title=_("Send Message"), form=form, recipient=recipient
    )


@app.route("/messages")
@login_required
def messages():
    current_user.last_message_read_time = datetime.now(timezone.utc)
    db.session.commit()
    page = request.args.get("page", 1, type=int)
    query = current_user.messages_received.select().order_by(Message.timestamp.desc())
    messages = db.paginate(
        query, page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False
    )
    next_url = (
        url_for("messages", page=messages.next_num) if messages.has_next else None
    )
    prev_url = (
        url_for("messages", page=messages.prev_num) if messages.has_prev else None
    )
    return render_template(
        "messages.html", messages=messages.items, next_url=next_url, prev_url=prev_url
    )
