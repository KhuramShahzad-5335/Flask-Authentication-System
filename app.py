from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

db_url = MongoClient('mongodb+srv://krshahzad786:KR5335sh@visperai.up1vsyk.mongodb.net/')


db = db_url.auth
collection = db.user_auth

# check if database is connected
print(db.list_collection_names())




app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret'



@app.route('/')
def home(): 
    if 'username' not in session:
        return redirect("/login")
    else:
        return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if 'username' not in session:
            session['username'] = None
        if 'password' not in session:
            session['password'] = None
        if (collection.find_one({"username": username, "password": password})) is not None:
            session['username'] = username
            session['password'] = password
            return redirect("/")
        else:
            print("Invalid username"+ username + password)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            username = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if 'username' == collection.find_one({"username": username}):
                return redirect("/login")
            if password == confirm_password:
                collection.insert_one({"username": username, "password": password})
                return redirect("/login")
            
        
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)