from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.models import *

config = Config("config.json")
DATABASE_URI = config.get_database_uri()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

db = SQLAlchemy(app)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)