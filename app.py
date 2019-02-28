from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort, request)
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

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


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
    return render_template('detail.html', entry=entry, tag=tag, resource=resource)


@app.route('/edit.html/<int:entry_id>', methods=('GET', 'POST'))
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
def delete_entry(entry_id, decision=None):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    for data in entry:
        tag = data.tags
        tag = tag.split()
        resource = data.resources
        resource = resource.split()
    if decision:
        models.Entries.delete().where(models.Entries.id == entry_id).execute()
        return redirect(url_for('index'))
    return render_template('delete.html', entry=entry, tag=tag, resource=resource)


@app.route('/new.html', methods=['GET', 'POST'])
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
        flash("Message posted! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
