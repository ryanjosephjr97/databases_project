from flask import Flask, render_template, request
app = Flask(__name__)


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


@app.route('/search-items')
def search-items():
  return render_template("search-items.html")


@app.route('/auctions')
def auctions():
  return render_template("auctions.html")


if __name__ == "__main__":
  app.run();
