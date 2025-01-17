from flask import Blueprint, request, render_template, redirect
from app.models import db, Member, Class, Payment
from app.services.payment_service import process_payment
from app.services.reservation_sevice import reserve_class
from datetime import datetime, timezone

members_bp = Blueprint('members', __name__)

@members_bp.route("/members", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        member_name = request.form["member_name"]
        member_phone = request.form["member_phone"]
        member_email = request.form["member_email"]

        if Member.query.filter_by(email=member_email).first():
            raise ValueError(f"Member with email {member_email} already exists.")
        
        new_member = Member(name=member_name, phone=member_phone, email=member_email)

        try:
            db.session.add(new_member)
            db.session.commit()
            return redirect("/members")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue adding the member: {str(e)}"

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

@members_bp.route("/members/delete/<int:id>")
def delete_member(id):
    member_to_delete = Member.query.get_or_404(id)

    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        return redirect("/members")
    except Exception as e:
        return f"There was a problem deleting the member: {str(e)}"
    
@members_bp.route("/members/update/<int:id>", methods=["POST", "GET"])
def update(id):
    member_to_update = Member.query.get_or_404(id)

    if request.method == "POST":
        member_to_update.name = request.form["member_name"]
        member_to_update.phone = request.form["member_phone"]
        member_to_update.email = request.form["member_email"]

        if Member.query.filter(Member.email == member_to_update.email, Member.id != member_to_update.id).first():
            raise ValueError(f"Member with email {member_to_update.email} already exists.")

        try:
            db.session.commit()
            return redirect("/members")
        except Exception as e:
            db.session.rollback()
            return f"There was an issue updating the member: {str(e)}"
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
            return f"There was an issue processing the payment: {str(e)}"
    else:
        payments = Payment.query.filter(Payment.member_id == id).all()
        return render_template("payment.html", member=member, payments=payments)