from flask import Flask
from flask import render_template
from flask.ext.neo4j import Neo4j
from py2neo import neo4j

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("layout.html", title="Home")


@app.route("/repo/register")
def repo_register():
    pass


@app.route("/repo/commit")
def repo_commit():
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()
