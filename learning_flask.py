from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user"
app.config["ALCHEMY_TRACK_MODIFICATION"] = False
app.config["SECRET_KEY"] = "Billprovip"
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email
        

#return thẻ html <h1>   </h1>
@app.route('/')
def Hello():
    return render_template('index.html', content = 'Nam Anh', 
                           cars = ['Merc', 'BMW','Bently'])


@app.route('/admin')
def hello_admin():
    return f'<h1> Hello admin </h1>'

#return redirect (chuyển hướng)
@app.route('/user/<name>')
def user_name(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    #return theo biến -> route
    return f"<h1>Hello {name}</h1>"


#return type 
@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    return f'<h1>Blog {blog_id}</h1>'

#Inheritance (Kế thừa)
@app.route('/home')
def home():
    return render_template('home.html')



#HTTP Method, POST, GET
@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            found_user = User.query.filter_by(name = user_name).first()
            if found_user:
                session["email"] = found_user.email
            else:
                user = User(user_name, "temp@gmail.com")
                db.session.add(user)
                db.session.commit()
                flash("Created in Database", "info")
            return redirect(url_for("user", user = user_name))
    #logic remain /login
    if "user" in session:
        name = session["user"]
        flash("You have already loged in", 'info')
        return redirect(url_for("user", user = user_name))
    return render_template('login.html')



#session
@app.route('/user', methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        name = session["user"]
        if request.method == "POST":
            if not request.form["email"] and request.form["name"]:
                User.query.filter_by(name = name).delete()
                db.session.commit()
                flash("Deleted User")
                return redirect(url_for("logout"))
            else:
                email = request.form["email"]
                session["email"] = email
                found_user = User.query.filter_by(name = name).first()
                found_user.email = email
                db.session.commit()
                flash("Email updated")
        elif "email" in session:
                email = session["email"]
        return render_template("user.html", user = name, email = email)
    else:
        flash("You haven't logged in yet")
        return redirect(url_for("login"))
    

#logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("Log out Succesfully", 'info')
    return redirect(url_for("login"))



#
if __name__ == "__main__":
    def create_database(app):
        if not path.exists("db.user"):
            with app.app_context():
                db.create_all()
                print('Created Database!')
    create_database(app)
    app.run(debug=True)



