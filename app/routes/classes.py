from flask import Blueprint, request, render_template, redirect
from app.models import db, Class, Trainer
from datetime import datetime

classes_bp = Blueprint('classes', __name__)

@classes_bp.route("/classes", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        class_trainer_id = request.form["class_trainer_id"]
        class_name = request.form["class_name"]
        class_capacity = request.form["class_capacity"]
        class_start_time = request.form["class_start_time"]

        """
        pridat kontrolu na cas a kapacitu do services
        """
        
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
    class_to_delete = Class.query.get_or_404(id)

    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        return redirect("/classes")
    except Exception as e:
        return f"There was a problem deleting the class: {str(e)}"