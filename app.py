from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['SECRET_KEY'] = "rtgwrhg543643554frg4234r4ferf234"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/index.html')
@app.route('/index.html/<tag>')
def index(tag=None):
    data = models.Entries.select()
    if tag:
        data = models.Entries.select().where(models.Entries.tags.contains(tag))
    return render_template('index.html', data=data)


@app.route('/detail_page/<int:entry_id>')
def detail_page(entry_id):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    for data in entry:
        tag = data.tags
        tag = tag.split()
        resource = data.resources
        resource = resource.split()
    return render_template('detail.html', entry=entry,
                           tag=tag, resource=resource)


@app.route('/edit.html/<int:entry_id>', methods=('GET', 'POST'))
@login_required
def edit_entry(entry_id):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    form = forms.EntryForm()
    if form.validate_on_submit():
        entry_id = request.form['entry_id']
        update = models.Entries.update(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data,
            tags=form.tags.data).where(models.Entries.id == entry_id)
        update.execute()
        flash("Entry edited!", "success")
        return redirect(url_for('index'))
    for value in entry:
        form.title.default = value.title
        form.date.default = value.date
        form.time_spent.default = value.time_spent
        form.learned.default = value.learned
        form.resources.default = value.resources
        form.tags.default = value.tags
    form.process()
    return render_template('edit.html', entry=entry, form=form)


@app.route('/delete_entry/<int:entry_id>')
@app.route('/delete_entry/<int:entry_id>/<decision>')
@login_required
def delete_entry(entry_id, decision=None):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    for data in entry:
        tag = data.tags
        tag = tag.split()
        resource = data.resources
        resource = resource.split()
    if decision:
        models.Entries.delete().where(models.Entries.id == entry_id).execute()
        flash("Entry deleted!", "success")
        return redirect(url_for('index'))
    return render_template('delete.html', entry=entry,
                           tag=tag, resource=resource)


@app.route('/new.html', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entries.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data,
            tags=form.tags.data
        )
        flash("Entry added!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
