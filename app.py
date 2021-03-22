from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    logging,
    session,
    g,
    Response,
) 
import sqlite3
from markupsafe import escape
import secrets
from db import (DB, BadRequest, KeyNotFound, UsernameAlreadyExists)

# Configure application
app = Flask(__name__)

# path to database
DATABASE = './database.db'

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secrets.token_urlsafe(50)

# default path
@app.route("/")
def home(message = None):
    if not check_logged_in():
        return redirect(url_for('login'))
    app.logger.debug('Logged in as {} with message {}'.format(escape(session['username']), message))
    db = DB(get_db())
    myexpenses = None
    try:
        myexpenses = db.myexpenses(session['username'])
        print(myexpenses)
    except BadRequest as e:
        app.logger.error(f"{e}")
    return render_template("myexpenses.html", rows=myexpenses, message=message, user=escape(session['username']))

########################################
## login endpoints                    ##
########################################

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            db = DB(get_db())
            try:
                if db.validate_user(request):
                    session['username'] = request.form['username']
                else:
                    error = 'Invalid Credentials. Please try again.'
                    return render_template('login.html', newuser=False, error=error)
            except Exception as e:
                app.logger.error(e)
                error = 'Invalid Credentials. Please try again.'
                return render_template('login.html', newuser=False, error=error)
            return redirect(url_for('home'))
        else:
            error = 'Username or Password was empty. Please try again.'
    return render_template('login.html', newuser=False, error=error)

@app.route("/newuser", methods=["GET", "POST"])
def createuser():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            db = DB(get_db())
            try:
                db.add_user(request)
                session['username'] = request.form['username']
            except UsernameAlreadyExists as e:
                app.logger.error(e.message)
                error = "Username already exists. Try a different one."
                return render_template('login.html', newuser=True, error=error)
            except Exception as e:
                app.logger.error(e)
                return render_template('login.html', newuser=True, error=e)
            return redirect(url_for('home'))
        else:
            error = 'Username or Password was empty. Please try again.'
    return render_template('login.html', newuser=True, error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


########################################
## Spending endpoints                 ##
########################################

@app.route('/addspending', methods=['POST'])
def addspending():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = "Spending added successfully"
    try:
        db.addspending(session['username'], request)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Add spending failed. Make user form input is correct"
    return redirect(url_for('myspending'))

@app.route('/myspending', methods=['Get'])
def myspending():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = None
    myspending = None
    try:
        myspending = db.myspending(session['username'])
        print(myspending)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Something went wrong. Please try again"
    return render_template("myspending.html", rows=myspending, message=message)


########################################
## Expense endpoints                  ##
########################################

@app.route('/addexpense', methods=['POST'])
def addexpense():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = "Expense added successfully"
    try:
        db.addexpense(session['username'], request)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Add expense failed. Make user form input is correct"
    return redirect(url_for('myexpenses'))

@app.route('/myexpenses', methods=['Get'])
def myexpenses():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = None
    myexpenses = None
    try:
        myexpenses = db.myexpenses(session['username'])
        print(myexpenses)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Something went wrong. Please try again"
    return render_template("myexpenses.html", rows=myexpenses, message=message)


########################################
## Goal endpoints                     ##
########################################

@app.route('/addgoal', methods=['POST'])
def addgoal():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = "goal added successfully"
    try:
        db.addgoal(session['username'], request)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Add goal failed. Make user form input is correct"
    return redirect(url_for('mygoals'))

@app.route('/mygoals', methods=['Get'])
def mygoals():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = None
    mygoals = None
    try:
        mygoals = db.mygoals(session['username'])
        print(mygoals)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Something went wrong. Please try again"
    return render_template("mygoals.html", rows=mygoals, message=message)


########################################
## Debt endpoints                     ##
########################################

@app.route('/adddebt', methods=['POST'])
def adddebt():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = "Debt added successfully"
    try:
        db.adddebt(session['username'], request)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Add Debt failed. Make user form input is correct"
    return redirect(url_for('mydebt'))

@app.route('/mydebt', methods=['Get'])
def mydebt():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = None
    mydebt = None
    try:
        mydebt = db.mydebt(session['username'])
        print(mydebt)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Something went wrong. Please try again"
    return render_template("mydebt.html", rows=mydebt, message=message)


########################################
## Income endpoints                   ##
########################################

@app.route('/addincome', methods=['POST'])
def addincome():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = "Income added successfully"
    try:
        db.addincome(session['username'], request)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Add income failed. Make user form input is correct"
    return redirect(url_for('myincome'))

@app.route('/myincome', methods=['Get'])
def myincome():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = None
    myincome = None
    try:
        myincome = db.myincome(session['username'])
        print(myincome)
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Something went wrong. Please try again"
    return render_template("myincome.html", rows=myincome, message=message)


########################################
## Combination endpoints              ##
########################################


########################################
## Import endpoints                   ##
########################################
@app.route('/importcsv', methods=['GET', 'POST'])
def importcsv():
    if not check_logged_in():
        return redirect(url_for('login'))
    db = DB(get_db())
    message = None
    try:
        db.import_csvdata(session['username'], request.form['csvfile'], request.form['tablename'])
    except BadRequest as e:
        app.logger.error(f"{e}")
        message = "Something went wrong. Please try again"
    return redirect(url_for("my{}".format(request.form['tablename']), message=message))


########################################
## Utility functions                  ##
########################################

def check_logged_in():
    if 'username' in session:
        print("you are logged in! " + session['username'])
        return True
    print("go log in")
    return False

# connect to db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# close connectiong to db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create Database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    

if __name__ == "__main__":
    app.run(debug=True)