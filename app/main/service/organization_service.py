import datetime

from main import db
from main.model.organization import Organization
from main.service.bill_service import getBillById, create_new_bill


def getAllOrganization():
    organizations = Organization.query.all()
    for organization in organizations:
        organization.bill = getBillById(organization.bill_id)
    return organizations


def getOrganizationById(organization_id):
    if organization_id:
        organization = Organization.query.filter_by(id=organization_id).first()
        organization.bill = getBillById(organization.bill_id)
        return organization
    return None


def create_new_organization(data):
    bill = create_new_bill(data)
    organization = Organization(
        name=data["name"],
        siret=data["siret"],
        address=data["address"],
        creation_date=datetime.datetime.now(),
        bill_id= bill["id"]
    )
    save_changes(organization)
    db.session.refresh(organization)
    return {"id": organization.id, "name": organization.name, "status": "success", "message": "Organization inserted"}


def update_organization(report_id, data):
    return {"status": "teapot", "message": "I'm a teapot"}, 418


def delete_organization(report_id):
    return {"status": "teapot", "message": "I'm a teapot"}, 418


def save_changes(data):
    db.session.add(data)
    db.session.commit()
