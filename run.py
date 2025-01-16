from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, ConfigError
from app.models import *

app = Flask(__name__)

try:
    config = Config("config.json")
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
except ConfigError as e:
    print(f"Configuration error: {e}")
    exit(1)

db.init_app(app)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        member_name = request.form["member_name"]
        member_phone = request.form["member_phone"]
        member_email = request.form["member_email"]
        
        member = Member(name=member_name, phone=member_phone, email=member_email)

        try:
            db.session.add(member)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue adding the member: {str(e)}"

    else:
        members = Member.query.order_by(Member.registration_date).all()
        return render_template("index.html", members=members)
    
@app.route("/delete/<int:id>")
def delete(id):
    member_to_delete = Member.query.get_or_404(id)

    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was a problem deleting the member: {str(e)}"

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    member_to_update = Member.query.get_or_404(id)

    if request.method == "POST":
        member_to_update.name = request.form["member_name"]
        member_to_update.phone = request.form["member_phone"]
        member_to_update.email = request.form["member_email"]

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue updating the member: {str(e)}"
    else:
        return render_template("update.html", member=member_to_update)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)