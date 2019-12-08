# project/server/user/views.py


from flask import (
    render_template, Blueprint, url_for, redirect, flash, request,
    abort, jsonify, session, g)
from flask_login import login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm


user_blueprint = Blueprint("user", __name__)


@user_blueprint.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Thank you for registering.", "success")
        return redirect(url_for("user.members"))

    return render_template("user/register.html", form=form)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, request.form["password"]
        ):
            login_user(user)
            session['user_id'] = user.id
            flash("You are logged in. Welcome!", "success")
            return redirect(url_for("user.members"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", title="Please Login", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("main.home"))


@user_blueprint.route("/members")
@login_required
def members():
    return render_template("user/members.html")


@user_blueprint.route('/users/')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user/list.html', users=users)


@user_blueprint.route('/users/<int:user_id>/')
@login_required
def user_detail(user_id):
    user = User.query.get(user_id)
    return render_template('user/detail.html', user=user)


@user_blueprint.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)


@user_blueprint.route('/users/create/', methods=['GET', 'POST'])
@login_required
def user_create():
    if request.method == 'POST':
        user = User(name=request.form['name'],
                    email=request.form['email'],
                    password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.user_list'))
    return render_template('user/edit.html')


@user_blueprint.route('/users/<int:user_id>/delete/', methods=['DELETE'])
def user_delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'OK'})
