from flask import Blueprint, request, render_template, redirect, flash
from app.models import db, Member, Class, Reservation, Payment
from app.services.reservation_sevice import reserve_class
from datetime import datetime, timezone

reservation_bp = Blueprint('reservation', __name__)
  
@reservation_bp.route("/reservation/<int:member_id>", methods=["POST", "GET"])
def reservation(member_id):
    """
    Vytváří stránku rezervací lekcí a zpracovává vytváření nových rezervací.
    """
    member = Member.query.get_or_404(member_id)

    if request.method == "POST":
        try:
            class_id = request.form["class_id"]

            message = reserve_class(member.id, class_id)

            return render_template('reservation_success.html', message=message)
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue adding the reservation: {str(e)}")
            return redirect(f"/reservation/{member_id}")
    else:
        classes = Class.query.filter(Class.start_time > datetime.now(timezone.utc)).all()
        reservations = Reservation.query.filter(Reservation.member_id == member_id, Reservation.reservation_time > datetime.now(timezone.utc)).all()
        return render_template("reservation.html", member=member, classes=classes, reservations=reservations)
    

@reservation_bp.route('/reservation/<int:member_id>', methods=['GET'])
def get_reservations_for_member(member_id):
    """
    Vrátí stránku aktvních rezervací pro konkrétního člena.
    """
    member = Member.query.get(member_id)
    if not member:
        flash(f"Member does not exist.")
        return redirect("/members")

    reservations = Reservation.query.filter(Reservation.member_id == member_id, Reservation.reservation_time > datetime.now(timezone.utc)).all()

    return render_template('reservation.html', member=member, reservations=reservations)

@reservation_bp.route('/reservation/delete/<int:id>')
def delete_reservation(id):
    """
    Odstraní rezervaci lekce z databáze.
    """
    reservation_to_delete = Reservation.query.get_or_404(id)

    reservation_to_delete.class_info.capacity += 1

    try:
        db.session.delete(reservation_to_delete)
        db.session.commit()
        return redirect("/members")
    except Exception as e:
        
        return f"There was a problem deleting the reservation: {str(e)}"