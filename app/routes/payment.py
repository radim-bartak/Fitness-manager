from flask import Blueprint, render_template, request
from app.services.payment_service import process_payment
from app.models import Member

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            member_id = request.form['member_id']
            amount = float(request.form['amount'])
            payment_method = request.form['payment_method']
            membership_type = request.form['membership_type']
            valid_from = request.form['valid_from']
            valid_to = request.form['valid_to']

            # Zpracování platby a vytvoření členství
            message = process_payment(member_id, amount, payment_method, membership_type, valid_from, valid_to)

            # Zobrazení úspěšné zprávy
            return render_template('payment_success.html', message=message)

        except Exception as e:
            return render_template('payment_form.html', error=str(e), members=Member.query.all())

    # Zobrazení formuláře
    return render_template('payment_form.html', members=Member.query.all())