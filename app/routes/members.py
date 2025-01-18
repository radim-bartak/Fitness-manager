from flask import Blueprint, request, render_template, redirect, flash
from app.models import db, Member, Class, Payment
from app.services.payment_service import process_payment
from app.services.reservation_sevice import reserve_class
from datetime import datetime, timezone
import csv
import io
import re

members_bp = Blueprint('members', __name__)

@members_bp.route("/members", methods=["POST", "GET"])
def index():
    """
    Vytváří stránku členů a zpracovává vytváření nových členů.
    """
    if request.method == "POST":
        member_name = request.form["member_name"]
        member_phone = request.form["member_phone"]
        member_email = request.form["member_email"]

        if Member.query.filter_by(email=member_email).first():
            flash(f"Member with email {member_email} already exists.")
            return redirect("/members")
        
        new_member = Member(name=member_name, phone=member_phone, email=member_email)

        try:
            db.session.add(new_member)
            db.session.commit()
            return redirect("/members")
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue adding the member: {str(e)}")
            return redirect("/members")

    else:
        search_name = request.args.get("search_name")
        search_email = request.args.get("search_email")
        search_phone = request.args.get("search_phone")
        if search_name:
            members = Member.query.filter(Member.name.ilike(f"%{search_name}%")).order_by(Member.registration_date).all()
        elif search_email:
            members = Member.query.filter(Member.email.ilike(f"%{search_email}%")).order_by(Member.registration_date).all()
        elif search_phone:
            members = Member.query.filter(Member.phone.ilike(f"%{search_phone}%")).order_by(Member.registration_date).all()
        else:
            members = Member.query.order_by(Member.registration_date).all()
        return render_template("members.html", members=members)

@members_bp.route("/members/import", methods=["POST"])
def import_members():
    """
    Importuje členy z CSV souboru.
    """
    if 'csv_file' not in request.files:
        flash('No file part')
        return redirect("/members")
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No selected file')
        return redirect("/members")
    
    if file and file.filename.endswith('.csv'):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        for row in csv_input:
            if len(row) != 3:
                flash('Invalid CSV format. Each row must have 3 columns: name, phone, email.')
                return redirect("/members")
            member_name, member_phone, member_email = row
            
            if not member_name  or not member_phone or not member_email:
                flash('All fields (name, phone, email) are required.')
                return redirect("/members")
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", member_email):
                flash(f'Invalid email format: {member_email}')
                return redirect("/members")
            
            if Member.query.filter_by(email=member_email).first():
                continue
            
            new_member = Member(name=member_name, phone=member_phone, email=member_email)
            db.session.add(new_member)
        db.session.commit()
        flash('Members imported successfully')
    else:
        flash('Invalid file format. Please upload a CSV file.')
    
    return redirect("/members")

@members_bp.route("/members/delete/<int:id>")
def delete_member(id):
    """
    Odstraní člena z databáze.
    """
    member_to_delete = Member.query.get_or_404(id)

    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        return redirect("/members")
    except Exception as e:
        return f"There was a problem deleting the member: {str(e)}"
    
@members_bp.route("/members/update/<int:id>", methods=["POST", "GET"])
def update(id):
    """
    Upraví člena v databázi.
    """
    member_to_update = Member.query.get_or_404(id)

    if request.method == "POST":
        member_to_update.name = request.form["member_name"]
        member_to_update.phone = request.form["member_phone"]
        member_to_update.email = request.form["member_email"]

        if Member.query.filter(Member.email == member_to_update.email, Member.id != member_to_update.id).first():
            flash(f"Member with email {member_to_update.email} already exists.")
            return redirect(f"/members/update/{id}")

        try:
            db.session.commit()
            return redirect("/members")
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue updating the member: {str(e)}")
            return redirect(f"/members/update/{id}")
    else:
        return render_template("update_member.html", member=member_to_update)
    
@members_bp.route("/members/payment/<int:id>", methods=["POST", "GET"])
def payment(id):
    member = Member.query.get_or_404(id)

    if request.method == "POST":
        try:
            total_price = float(request.form["total_price"])
            payment_method = request.form["payment_method"]
            membership_type = request.form["membership_type"]

            message = process_payment(member.id, total_price, payment_method, membership_type)

            return render_template('payment_success.html', message=message)
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue processing the payment: {str(e)}")
            return redirect(f"/members")
    else:
        payments = Payment.query.filter(Payment.member_id == id).all()
        return render_template("payment.html", member=member, payments=payments)