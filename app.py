import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, g
from random import randint
app = Flask(__name__)

IP_ADDR = "35.194.34.244"


@app.route('/')
def homepage():
  return render_template("homepage.html")


@app.route('/create-account')
def create-account():
  return render_template("create-account.html")


@app.route('/sign-in')
def sign-in():
  return render_template("sign-in.html")


@app.route('/user-home')
def user-home():
  return render_template("user-home.html")


@app.route('/messages')
def messages():
  return render_template("messages.html")


@app.route('/post-item')
def post-item():
  return render_template("post-item.html")


@app.route('/view-item')
def view-item():
  return render_template("view-item.html")


@app.route("/search-item", methods=["get", "post"])
def search():
    if "query" not in request.form:
        return render_template("search-item.html")
    else:
        db = get_db()
        cursor = db.cursor()
        query = str(request.form["query"])
        sql_query = "select * from item_types natural join items natural join category" + \
            " where LOWER(catname)=LOWER('" + query + "') or " + \
            "LOWER(itemname) like LOWER(" + "'%" + query + "%') or " + \
            "LOWER(description) like LOWER('%" + query + "%')"
        print(sql_query)

        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return render_template("search-item.html", entries=rows)


@app.route('/auctions')
def auctions():
  return render_template("auctions.html")

# ------------------------------------------

# Database handling


def connect_db():
    """Connects to the database."""
    debug("Connecting to DB.")
    conn = psycopg2.connect(host=IP_ADDR, user="postgres", password="rhodes"
        , dbname="exchangedb", cursor_factory=psycopg2.extras.DictCursor)
    return conn


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database automatically when the application
    context ends."""
    debug("Disconnecting from DB.")
    if hasattr(g, 'pg_db'):
        g.pg_db.close()


def debug(s):
    """Prints a message to the screen if FLASK_DEBUG is set."""
    if app.config['DEBUG']:
        print(s)
