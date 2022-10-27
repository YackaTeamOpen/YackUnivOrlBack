from flask_login import current_user

from main import db
from main.model.bill import Bill


def getAllBill():
    return Bill.query.all()


def getBillById(bill_id):
    return Bill.query.filter_by(id=bill_id).first()


def create_new_bill(data):
    if current_user.type == 0:
        bill = Bill(
            price=data["price"],
            nb_max_employees=data["nb_max_employees"],
        )
        save_changes(bill)
        db.session.refresh(bill)
        return {"id": bill.id, "status": "success", "message": "Bill inserted"}
    return {"status": "fail", "message": "Unauthorized"}, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
