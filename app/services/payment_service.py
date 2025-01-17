from flask import flash, redirect
from app.models import db, Payment, Member, Membership
from datetime import datetime, timedelta, date

def process_payment(member_id, amount, payment_method, membership_type):
    """
    Zpracuje platbu, vytvoří členství a aktualizuje stav člena.

    :param member_id: ID člena
    :param amount: Částka platby
    :param payment_method: Způsob platby ('Cash', 'Card', 'Online')
    :param membership_type: Typ členství ('Monthly', Three-month, 'Yearly')
    :return: Zpráva o úspěchu nebo vyhození chyby
    """
    now = datetime.utcnow()

    if amount <= 0:
        flash(f"Amount must be a positive number.")
        return redirect(f"/members/payment/{member_id}")

    member = Member.query.get(member_id)
    if not member:
        flash(f"Member does not exist.")
        return redirect(f"/members/payment/{member_id}")

    valid_from = datetime.utcnow()
    if membership_type == 'Monthly':
        valid_to = valid_from + timedelta(days=30)
    elif membership_type == 'Three-month':
        valid_to = valid_from + timedelta(days=90)
    elif membership_type == 'Yearly':
        valid_to = valid_from + timedelta(days=365)
    else:
        raise ValueError(f"Invalid type of membership: {membership_type}")
    
    existing_memberships = Membership.query.filter_by(member_id=member_id).all()
    if existing_memberships:
        for existing_membership in existing_memberships:
            if existing_membership.valid_to > now:
                flash(f"Member already has an active membership.")
                return redirect(f"/members/payment/{member_id}")

    membership = Membership(
        member_id=member_id,
        type=membership_type,
        price=amount,
        valid_from=valid_from,
        valid_to=valid_to
    )
    db.session.add(membership)
    db.session.flush()
    
    payment = Payment(
        member_id=member_id,
        membership_id=membership.id,
        total_price=amount,
        payment_method=payment_method
    )
    db.session.add(payment)
    
    member.active_membership = True

    db.session.commit()
    return f"Payment in the amount {amount} was successful. {member.name} now has a {membership_type} membership."