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

    member = Member.query.get(member_id)
    if not member:
        raise ValueError(f"Člen s ID {member_id} neexistuje.")

    valid_from = datetime.utcnow()
    if membership_type == 'Monthly':
        valid_to = valid_from + timedelta(days=30)
    elif membership_type == 'Three-month':
        valid_to = valid_from + timedelta(days=90)
    elif membership_type == 'Yearly':
        valid_to = valid_from + timedelta(days=365)
    else:
        raise ValueError(f"Neplatný typ členství: {membership_type}")

    membership = Membership(
        member_id=member_id,
        type=membership_type,
        price=amount,
        valid_from=valid_from,
        valid_to=valid_to
    )
    db.session.add(membership)
    
    payment = Payment(
        member_id=member_id,
        membership_id=membership.id,
        total_price=amount,
        payment_method=payment_method
    )
    db.session.add(payment)
    
    member.active_membership = True

    db.session.commit()
    return f"Platba ve výši {amount} byla úspěšně zpracována a členství bylo vytvořeno."