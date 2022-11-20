from app import app
from flask import request, redirect, url_for, render_template, session, json
import ibm_db
from sendGrid import mailto, checkstatus, getProductsBelowThValue


#Connect to DB
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tjn82499;PWD=PKnjWIiY8zakBnmU",'','')

@app.route("/")
def root():
    return render_template("home.html", title="Home")


@app.route("/signin", methods=('POST', 'GET'))
def signin():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT username FROM users WHERE password = '{}' AND email = '{}'".format(password, email)
        stmt = ibm_db.exec_immediate(conn, sql)
        fetchUser = ibm_db.fetch_assoc(stmt)
        if fetchUser == False:
            error = "Incorrect Username/Password."

        if error is None:
            user = fetchUser["USERNAME"]
            session['loggedIn'] = True
            session['id'] = user
            session['email'] = email
            return redirect(url_for('.dashboard', username=user))
    return render_template('signin.html', error=error)


@app.route("/signup", methods=('POST', 'GET'))
def signup():
    error=None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        checkUser = "SELECT * FROM users WHERE username = '{}'".format(username)
        stmt = ibm_db.exec_immediate(conn, checkUser)
        findUser = ibm_db.fetch_assoc(stmt)
        if findUser == False:
            sql = "INSERT INTO users (email, username, password) VALUES ('{}', '{}', '{}');".format(email, username, password)
            ibm_db.exec_immediate(conn, sql)
            return render_template('home.html', title="Home", isRegistered=True)
        error="Username aldready exists."
    return render_template("signup.html", error=error)




@app.route('/')
def logout():
   session.clear()
   return render_template('home.html')
