from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort, request)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from peewee import *

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'wegrtgwrhg543643554frg4234r4ferf234'


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
        data = models.Entries.select().where(models.Entries.tags == tag)
    return render_template('index.html', data=data)


@app.route('/detail_page/<int:entry_id>')
def detail_page(entry_id):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    return render_template('detail.html', entry=entry)


@app.route('/edit.html/<int:entry_id>', methods=('GET', 'POST'))
def edit_entry(entry_id):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    if request.method == 'POST':
        entry_id = request.form['entry_id']
        update = models.Entries.update(
            title=request.form['title'],
            date=request.form['date'],
            time_spent=request.form['timeSpent'],
            learned=request.form['whatILearned'],
            resources=request.form['ResourcesToRemember'],
            tags=request.form['Tags']).where(models.Entries.id == entry_id)
        update.execute()
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)


@app.route('/delete_entry/<int:entry_id>')
@app.route('/delete_entry/<int:entry_id>/<decision>')
def delete_entry(entry_id, decision=None):
    entry = models.Entries.select().where(models.Entries.id == entry_id)
    if decision:
        models.Entries.delete().where(models.Entries.id == entry_id).execute()
        return redirect(url_for('index'))
    return render_template('delete.html', entry=entry)


@app.route('/new.html', methods=('GET', 'POST'))
def new_entry():
    if request.method == 'POST':
        models.Entries.create(
            title=request.form['title'],
            date=request.form['date'],
            time_spent=request.form['timeSpent'],
            learned=request.form['whatILearned'],
            resources=request.form['ResourcesToRemember'],
            tags=request.form['Tags']
        )
        return redirect(url_for('index'))
    return render_template('new.html')


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
