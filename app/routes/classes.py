from flask import Blueprint, request, render_template, redirect, flash
from app.models import db, Class, Trainer
from datetime import datetime

classes_bp = Blueprint('classes', __name__)

@classes_bp.route("/classes", methods=["POST", "GET"])
def index():
    """
    Vytváří stránku lekcí a zpracovává vytváření nových lekcí.
    """
    if request.method == "POST":
        class_trainer_id = request.form["class_trainer_id"]
        class_name = request.form["class_name"]
        class_capacity = request.form["class_capacity"]
        class_start_time = request.form["class_start_time"]

        if int(class_capacity) <= 0:
            flash('Class capacity must be a positive number.')
            return redirect("/classes")

        start_time = datetime.strptime(class_start_time, '%Y-%m-%dT%H:%M')
        if start_time <= datetime.now():
            flash('Class start time must be in the future.')
            return redirect("/classes")
        
        new_class = Class(trainer_id=class_trainer_id, name=class_name, capacity=class_capacity, start_time=class_start_time)

        try:
            db.session.add(new_class)
            db.session.commit()
            return redirect("/classes")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue adding the class: {str(e)}"

    else:
        classes = Class.query.order_by(Class.start_time).all()
        trainers = Trainer.query.order_by(Trainer.name).all()
        return render_template("classes.html", classes=classes, trainers=trainers)
    
@classes_bp.route("classes/delete/<int:id>")
def delete_class(id):
    """
    Odstraní lekci z databáze.
    """
    class_to_delete = Class.query.get_or_404(id)

    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        return redirect("/classes")
    except Exception as e:
        return f"There was a problem deleting the class: {str(e)}"
    
@classes_bp.route("classes/update/<int:id>", methods=["POST", "GET"])
def update(id):
    """
    Upraví lekci v databázi.
    """
    class_to_update = Class.query.get_or_404(id)
    trainers = Trainer.query.order_by(Trainer.name).all()

    if request.method == "POST":
        class_to_update.trainer_id = request.form["class_trainer_id"]
        class_to_update.name = request.form["class_name"]
        class_to_update.capacity = request.form["class_capacity"]
        class_to_update.start_time = request.form["class_start_time"]

        if int(class_to_update.capacity) <= 0:
            flash('Class capacity must be a positive number.')
            return redirect("/classes")
        
        start_time = datetime.strptime(class_to_update.start_time, '%Y-%m-%dT%H:%M')
        if start_time <= datetime.now():
            flash('Class start time must be in the future.')
            return redirect("/classes")

        try:
            db.session.commit()
            return redirect("/classes")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue updating the class: {str(e)}"

    return render_template("update_class.html", class_to_update=class_to_update, trainers=trainers)