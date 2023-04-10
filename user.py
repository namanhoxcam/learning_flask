
from flask import Blueprint
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta


user = Blueprint("user", __name__, static_folder="", template_folder="")
#static_folder="", template_folder="" -> put folder used into


#HTTP Method, POST, GET
@user.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            return redirect(url_for("user._user", user = user_name))
    #logic remain /login
    if "user" in session:
        name = session["user"]
        flash("You have already loged in", 'info')
        return redirect(url_for("user._user", user = user_name))
    return render_template('login.html')



#session
@user.route('/user', methods = ["POST", "GET"])
def _user():
    email = None
    if "user" in session:
        name = session["user"]
        return render_template("user.html", user = name)
    else:
        flash("You haven't logged in yet")
        return redirect(url_for("user.login"))
    

#logout
@user.route('/logout')
def logout():
    session.pop("user", None)
    flash("Log out Succesfully", 'info')
    return redirect(url_for("login"))
