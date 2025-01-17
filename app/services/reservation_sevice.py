from flask import flash, redirect
from app.models import db, Reservation, Member, Class
from datetime import datetime, date, time

def reserve_class(member_id, class_id):
    """
    Rezervuje lekci pro člena, pokud je kapacita dostupná.

    :param member_id: ID člena
    :param class_id: ID lekce
    :return: Zpráva o úspěchu nebo vyhození chyby
    """
    member = Member.query.get(member_id)
    if not member:
        flash(f"Member does not exist.")
        return redirect(f"/reservation/{member_id}")
    if member.active_membership == False:
        flash(f"Member {member.name} does not have an active membership.")
        return redirect(f"/reservation/{member_id}")

    class_info = Class.query.get(class_id)
    if not class_info:
        flash(f"Class {class_id} does not exist.")
        return redirect(f"/reservation/{member_id}")

    if class_info.capacity <= 0:
        flash(f"Class '{class_info.name}' is already full.")
        return redirect(f"/reservation/{member_id}")
    
    existing_reservation = Reservation.query.filter_by(member_id=member_id, class_id=class_id).first()
    if existing_reservation:
        flash("Member already has a reservation for this class.")
        return redirect(f"/reservation/{member_id}")

    reservation = Reservation(
        member_id=member_id,
        class_id=class_id,
        reservation_date= class_info.start_time,
        reservation_time= class_info.start_time
    )
    db.session.add(reservation)

    class_info.capacity -= 1

    db.session.commit()
    return f"Reservation of class '{class_info.name}' for {member.name} was successful."