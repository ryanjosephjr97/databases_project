import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, g
from random import randint
app = Flask(__name__)

IP_ADDR = "35.194.34.244"


@app.route('/')
def homepage():
  return render_template("homepage.html")


@app.route('/auctions', methods=['get', 'post'])
def auctions():
    if request.args:
        itemid = request.args.get('itemid')
        db = get_db()
        cursor = db.cursor()
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        cursor4 = db.cursor()
        sql_query = "select * from auction where itemselling=" + itemid
        cursor.execute(sql_query)
        row = cursor.fetchall()
        #debug(row)
        if len(row) > 0:
            auctionid = row[0][0]
            debug(auctionid)
            sql1 = "select * from bid where auctionid=" + str(auctionid)\
                + " Order by bidprice"
            #debug(sql1)
            cursor1.execute(sql1)
            bids = cursor1.fetchall()
            finalprice = bids[len(bids)-1][2]
            sql3 = "select * from chat where auctionid=" + str(auctionid)
            debug(sql3)
            cursor3.execute(sql3)
            chats = cursor3.fetchall()
            debug(bids)
            if "step" not in request.form:
                return render_template("auctions.html", step="no bid", fp=finalprice, auction=row[0], bids=bids, chats=chats)
            elif request.form["step"] == "add_entry":
                sql2 = "insert into bid(auctionId, bidder, bidPrice, bidTime) values ("\
                    + "'" + str(auctionid) + "'," + "'" + request.args.get("user") + "',"\
                    + "'" + request.form["bidamount"] + "', now())"
                debug(sql2)
                cursor2.execute(sql2)
                db.commit()
                cursor1.execute(sql1)
                bids = cursor1.fetchall()
                finalprice = bids[len(bids)-1][2]
                return render_template("auctions.html", fp=finalprice, auction=row[0], bids=bids, chats=chats)
            elif request.form["step"] == "add_chat":
                sql4 = "insert into chat(chatText, chatTime, chatter, auctionId) values ("\
                    + "'" + request.form["chattext"] + "', now(), '"\
                    + request.args.get("user") + "','" + str(auctionid) + "'" + ")"
                debug(sql4)
                cursor4.execute(sql4)
                db.commit()
                cursor3.execute(sql3)
                chats = cursor3.fetchall()
                return render_template("auctions.html", fp=finalprice, auction=row[0], bids=bids, chats=chats)
        else:
            return render_template("auctions.html", item=itemid, auction=row)
    else:
        return render_template("auctions.html")
      

@app.route('/create-account' methods=["post"])
def create-account():
    if "username" not in request.form:
        return render_template("create-account.html")
    else if "email" not in request.form:
        return render_template("create-account.html")
    else:
        db = get_db()
        cursor = db.cursor()
        username = str(request.form["username"])
        email = str(request.form["email"])
        cursor.execute("insert into users (email, username) values (%s, %s)",
                   str(request.form["email"], str(request.form["username"]])
        db.commit()
        return render_template("create-account.html")


@app.route('/sign-in')
def sign-in():
    if "username" not in request.form:
        return render_template("sign-in.html")
    else if "email" not in request.form:
        return render_template("sign-in.html")
    else:
        db = get_db()
        cursor = db.cursor()
        username = str(request.form["username"])
        username = str(request.form["email"])
        sql_query = "select * from users" + \
            " where username='" + username + "') and " + \
            "email like '" + email + "'"
        print(sql_query)

        cursor.execute(sql_query)
        user = cursor.fetchall()
        print(user)
        return render_template("search-item.html" user=user)


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
