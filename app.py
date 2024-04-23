from flask import Flask, render_template, flash, redirect, request, url_for, session, logging, redirect, abort
#from artical_data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NotSoSecretKey'

#Articles = Articles()

@app.route('/')
def HTML():
    return render_template('HTML.html')
    
@app.route('/recipes.html')
def recipes():
    return render_template('recipes.html')

@app.route('/new_restaurants')
def new_restaurants():
    return render_template('new_restaurants.html')

@app.route('/cuisine.html')
def cuisine():
    return render_template('cuisine.html')

@app.route('/account.html')
def account():
    return render_template('account.html')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/blog')
def blog():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('blog.html', posts=posts)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('blog'))

    return render_template('create.html')

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('blog'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('blog'))

if __name__ == '__main__':
    app.secret_key = 'Secret145'
    app.run(debug=True)
