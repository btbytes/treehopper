from flask import Flask
from flask import render_template
from flask.ext.neo4j import Neo4j
from py2neo import neo4j

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("home.html", title="Home")


@app.route("/user/")
def user_page():
    return render_template("user.html", title="User")


if __name__ == "__main__":
    app.debug = True
    app.run()
