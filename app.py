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
def index():
    data = models.Entries.select()
    return render_template('index.html', data=data)


@app.route('/detail_page/<entry>')
def detail_page(entry):
    return render_template('detail.html', data=entry)


@app.route('/edit.html')
def edit_entry():
    pass


@app.route('/new.html', methods=('GET', 'POST'))
def new_entry():
    if request.method == 'POST':
        models.Entries.create(
            title=request.form['title'],
            date=request.form['date'],
            time_spent=request.form['timeSpent'],
            learned=request.form['whatILearned'],
            resources=request.form['ResourcesToRemember'],
            tags='Test'
        )
        return redirect(url_for('index'))
    return render_template('new.html')


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)