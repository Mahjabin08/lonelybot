from flask import Flask, render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
import json
local_server = True
with open("templates/config.json","r") as c:
    params = json.load(c)['params']
app = Flask(__name__)
app.secret_key = 'ghaurabin'
if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

db = SQLAlchemy(app)

#
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    phone_num = db.Column(db.String(12), unique=False, nullable=False)
    msz = db.Column(db.String(50), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=True)
    email = db.Column(db.String(20), unique=False, nullable=False)



@app.route("/")
def home():
    return render_template('home.html',params=params)

@app.route("/signup")
def signup():
    return render_template('signup.html',params=params)

@app.route("/signin",methods=["GET","POST"])
def signin():
    # if user already signed in
    if ('user' in session and session['user'] == params['admin_user']):
        return  render_template('main.html')
    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        # set the session
        if(username == params['admin_user'] and userpass == params['admin_pass']):
            session['user'] = username
            return  render_template('main.html')


    return render_template('signin.html',params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    return render_template('home.html')


@app.route("/main")
def main():
    return render_template('main.html',params=params)



@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if ( request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name,email=email,phone_num=phone,date= datetime.now(), msz = message)
        db.session.add(entry)
        db.session.commit()
        '''Fetch data and add it to the database'''
    return render_template('contact.html',params=params)


if __name__ == '__main__':
    app.run(debug=True)
