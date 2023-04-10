from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from user import user

app = Flask(__name__)
app.config["SECRET_KEY"] = "Billprovip"
app.permanent_session_lifetime = timedelta(minutes=1)
app.register_blueprint(user, url_prefix = "/user")
# using url_prefix force the URL runs if it has /user


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






#
if __name__ == "__main__":
    app.run(debug=True)



