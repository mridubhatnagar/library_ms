from app.extensions import db 
from app.models.members import Members 
from sqlalchemy import and_ 

def save_member_details(member):
    members = Members()
    members.first_name = member["firstName"]
    members.last_name = member["lastName"]
    members.contact_number = member["contactNumber"]
    members.email = member["email"]
    db.session.add(members)
    db.session.commit()
    print("Member details inserted in members table")
    
def check_if_memberID_exists(memberID):
    query = db.session.query(Members.member_id).filter(Members.member_id==memberID).all()
    for row in query:
        return row[0]
    return None 

def get_members():
    members = db.session.query(Members).all()
    result = []
    for row in members:
        result.append({"member_id": row.member_id,
                       "first_name": row.first_name,
                       "last_name": row.last_name,
                       "contact_number": row.contact_number,
                       "email": row.email})
    return result


def delete_member(member_id):
    query = db.session.query(Members).filter(Members.member_id==member_id).first()
    if query:
        db.session.delete(query)
        db.session.commit()
        return member_id 
    

def get_member(memberid):
    query = db.session.query(Members).filter(Members.member_id==memberid).all()
    for row in query:
        return {"member_id": row.member_id, 
                "first_name": row.first_name,
                "last_name": row.last_name,
                "contact_number": row.contact_number,
                "email": row.email}

def save_contact_details(member_id, email, contact_number):
    db.session.query(Members).filter(Members.member_id==member_id).update({"email": email,
                                                                           "contact_number": contact_number})
    db.session.commit()


def search_member(payload):
    member_id = payload["memberID"]
    query = db.session.query(Members).filter(Members.member_id == member_id).all()
    for row in query:
        return {"member_id": row.member_id, 
                "first_name": row.first_name,
                "last_name": row.last_name,
                "contact_number": row.contact_number,
                "email": row.email}
    return {"member_id": '', 
            "first_name": '',
            "last_name": '',
            "contact_number": '',
            "email": ''}

