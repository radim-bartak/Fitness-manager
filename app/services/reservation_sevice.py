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
        raise ValueError(f"Member does not exist.")
    if member.active_membership == False:
        raise ValueError(f"Member {member.name} does not have an active membership.")

    class_info = Class.query.get(class_id)
    if not class_info:
        raise ValueError(f"Class {class_id} does not exist.")

    if class_info.capacity <= 0:
        raise ValueError(f"Class '{class_info.name}' is already full.")
    
    existing_reservation = Reservation.query.filter_by(member_id=member_id, class_id=class_id).first()
    if existing_reservation:
        raise ValueError("Member already has a reservation for this class.")

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