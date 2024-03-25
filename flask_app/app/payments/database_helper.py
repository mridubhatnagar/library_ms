from app.extensions import db 
from app.models.payments import Payments 
from sqlalchemy import and_ , func


def save_payment_details(member_id, amount_paid):
    payments = Payments()
    payments.member_id = member_id
    payments.amount_paid = amount_paid
    db.session.add(payments)
    db.session.commit()


def check_total_debt(member_id):
    query = db.session.query(Payments, 
                            func.sum(Payments.amount_paid),
                            func.sum(Payments.amount_due)
                            ).filter(Payments.member_id == member_id).group_by(Payments.member_id)
    
    for row in query:
        debt = row[2] - row[1]
        return debt 