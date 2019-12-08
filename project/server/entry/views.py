# project/server/entry/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request
from flask_login import login_required

from project.server import db
from project.server.models import Entry


entry_blueprint = Blueprint("entry", __name__)


@entry_blueprint.route('/entries')
def show_entries():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template('entry/show_entries.html', entries=entries)


@entry_blueprint.route('/entries/add', methods=['POST'])
@login_required
def add_entry():
    entry = Entry(
            title=request.form['title'],
            text=request.form['text']
            )
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('entry.show_entries'))
