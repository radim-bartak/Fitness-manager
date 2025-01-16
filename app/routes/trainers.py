from flask import Blueprint, request, render_template, redirect
from app.models import db, Trainer
from datetime import datetime

trainers_bp = Blueprint('trainers', __name__)

@trainers_bp.route("/trainers", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        trainer_name = request.form["trainer_name"]
        trainer_specialization = request.form["trainer_specialization"]
        trainer_phone = request.form["trainer_phone"]
        trainer_email = request.form["trainer_email"]
        
        new_trainer = Trainer(name=trainer_name, specialization=trainer_specialization, phone=trainer_phone, email=trainer_email)

        try:
            db.session.add(new_trainer)
            db.session.commit()
            return redirect("/trainers")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue adding the trainer: {str(e)}"

    else:
        search_name = request.args.get("search_name")
        search_email = request.args.get("search_email")
        search_phone = request.args.get("search_phone")
        if search_name:
            trainers = Trainer.query.filter(Trainer.name.ilike(f"%{search_name}%")).order_by(Trainer.name).all()
        elif search_email:
            trainers = Trainer.query.filter(Trainer.email.ilike(f"%{search_email}%")).order_by(Trainer.name).all()
        elif search_phone:
            trainers = Trainer.query.filter(Trainer.phone.ilike(f"%{search_phone}%")).order_by(Trainer.name).all()
        else:
            trainers = Trainer.query.order_by(Trainer.name).all()
        return render_template("trainers.html", trainers=trainers)

@trainers_bp.route("trainers/delete/<int:id>")
def delete_trainer(id):
    trainer_to_delete = Trainer.query.get_or_404(id)

    try:
        db.session.delete(trainer_to_delete)
        db.session.commit()
        return redirect("/trainers")
    except Exception as e:
        return f"There was a problem deleting the trainer: {str(e)}"
    
@trainers_bp.route("trainers/update/<int:id>", methods=["POST", "GET"])
def update(id):
    trainer_to_update = Trainer.query.get_or_404(id)

    if request.method == "POST":
        trainer_to_update.name = request.form["trainer_name"]
        trainer_to_update.specialization = request.form["trainer_specialization"]
        trainer_to_update.phone = request.form["trainer_phone"]
        trainer_to_update.email = request.form["trainer_email"]

        try:
            db.session.commit()
            return redirect("/trainers")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue updating the trainer: {str(e)}"
    else:
        return render_template("update.html", trainer=trainer_to_update)