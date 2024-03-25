from flask import render_template, request
from app.payments import bp
from app.payments import database_helper


@bp.route('/save', methods=["POST"])
def save():
    response = request.get_json()
    member_id = response["memberID"]
    amount_paid = response["amountPaid"]
    database_helper.save_payment_details(member_id, amount_paid)
    return f"Amount Paid updated for Member ID: {member_id}"

