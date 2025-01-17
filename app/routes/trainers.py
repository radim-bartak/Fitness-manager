from flask import Blueprint, request, render_template, redirect, flash, Response
from app.models import db, Trainer
from datetime import datetime
import csv
import io
import re
from app.services.report_service import trainer_utilization_report

trainers_bp = Blueprint('trainers', __name__)

@trainers_bp.route("/trainers", methods=["POST", "GET"])
def index():
    """
    Vytváří stránku trenérů a zpracovává vytváření nových trenérů.
    """
    if request.method == "POST":
        trainer_name = request.form["trainer_name"]
        trainer_specialization = request.form["trainer_specialization"]
        trainer_phone = request.form["trainer_phone"]
        trainer_email = request.form["trainer_email"]

        if Trainer.query.filter_by(email=trainer_email).first():
            flash(f"Trainer with email {trainer_email} already exists.")
            return redirect("/trainers")
        
        new_trainer = Trainer(name=trainer_name, specialization=trainer_specialization, phone=trainer_phone, email=trainer_email)

        try:
            db.session.add(new_trainer)
            db.session.commit()
            return redirect("/trainers")
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue adding the trainer: {str(e)}")
            return redirect("/trainers")

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

@trainers_bp.route("/trainers/import", methods=["POST"])
def import_trainers():
    """
    Importuje trenéry z CSV souboru.
    """
    if 'csv_file' not in request.files:
        flash('No file part')
        return redirect("/trainers")
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No selected file')
        return redirect("/trainers")
    
    if file and file.filename.endswith('.csv'):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        for row in csv_input:
            if len(row) != 4:
                flash('Invalid CSV format. Each row must have 4 columns: name, specialization, phone, email.')
                return redirect("/trainers")
            
            trainer_name, trainer_specialization, trainer_phone, trainer_email = row
            
            if not trainer_name or not trainer_specialization or not trainer_phone or not trainer_email:
                flash('All fields (name, specialization, phone, email) are required.')
                return redirect("/trainers")
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", trainer_email):
                flash(f'Invalid email format: {trainer_email}')
                return redirect("/trainers")
            
            if Trainer.query.filter_by(email=trainer_email).first():
                continue
            
            new_trainer = Trainer(name=trainer_name, specialization=trainer_specialization, phone=trainer_phone, email=trainer_email)
            db.session.add(new_trainer)
        
        db.session.commit()
        flash('Trainers imported successfully')
    else:
        flash('Invalid file format. Please upload a CSV file.')
    
    return redirect("/trainers")

@trainers_bp.route("trainers/delete/<int:id>")
def delete_trainer(id):
    """
    Odstraní trenéra z databáze.
    """
    trainer_to_delete = Trainer.query.get_or_404(id)

    try:
        db.session.delete(trainer_to_delete)
        db.session.commit()
        return redirect("/trainers")
    except Exception as e:
        return f"There was a problem deleting the trainer: {str(e)}"
    
@trainers_bp.route("trainers/update/<int:id>", methods=["POST", "GET"])
def update(id):
    """
    Upraví trenéra v databázi.
    """
    trainer_to_update = Trainer.query.get_or_404(id)

    if request.method == "POST":
        trainer_to_update.name = request.form["trainer_name"]
        trainer_to_update.specialization = request.form["trainer_specialization"]
        trainer_to_update.phone = request.form["trainer_phone"]
        trainer_to_update.email = request.form["trainer_email"]

        if Trainer.query.filter(Trainer.email == trainer_to_update.email, Trainer.id != trainer_to_update.id).first():
            flash(f"Trainer with email {trainer_to_update.email} already exists.")
            return redirect(f"/trainers/update/{id}")

        try:
            db.session.commit()
            return redirect("/trainers")
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue updating the trainer: {str(e)}")
            return redirect(f"/trainers/update/{id}")
    else:
        return render_template("update_trainer.html", trainer=trainer_to_update)
    
@trainers_bp.route('/trainers/report', methods=['GET'])
def trainer_report():
    """
    Vrátí stránku s reportem o vytížení trenérů.
    """
    
    report_data = trainer_utilization_report()
    return render_template('trainer_report.html', report_data=report_data)

@trainers_bp.route('/trainers/report/export', methods=['GET'])
def export_trainer_report():
    """
    Exportuje report o vytížení trenérů do CSV souboru.
    """
    report_data = trainer_utilization_report()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["Trainer ID", "Trainer Name", "Specialization", "Total Classes", "Total Free Spots", "Total Reservations", "Average Utilization"])
    
    for row in report_data:
        writer.writerow([row["trainer_id"], row["trainer_name"], row["specialization"], row["total_classes"], row["total_free_spots"], row["total_reservations"], row["average_utilization"]])
    
    output.seek(0)
    
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=trainer_report.csv'
    return response