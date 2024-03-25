from flask import render_template, request
from app.members import bp
from app.members import database_helper


@bp.route('/')
def index():
    members = database_helper.get_members()
    return render_template('members/members.html', members=members)



@bp.route('/add_member')
def add_books():
    return render_template('members/add_member.html')


@bp.route('/save_member_details', methods=["POST"])
def save_member():
    request_payload = request.get_json()
    database_helper.save_member_details(request_payload)
    return "details saved"


@bp.route('/member/<member_id>', methods=["GET"])
def get_member(member_id):
    member_details = database_helper.get_member(member_id)
    return render_template('members/show_member.html', member_details=member_details)


    
@bp.route('/save', methods=["POST", "GET"])
def save():
    response = request.get_json()
    member_id = response["member_id"]
    email = response["email"]
    contact_number = response["contact_number"]
    database_helper.save_contact_details(member_id, email, contact_number)
    return f"Contact details saved for member ID: {member_id}"



@bp.route('/delete', methods=["POST"])
def delete():
    response = request.get_json()
    member_id = int(response["member_id"].split("_")[1])
    result = database_helper.delete_member(member_id)
    return f"{result} deleted from the database. Kindly refresh the page\
    to see updated list of books."


@bp.route('/search/member', methods=["POST"])
def search_member():
    response = request.get_json()
    result = database_helper.search_member(response)
    print("==========")
    print(result)
    return result




@bp.route('/search', methods=["GET"])
def search():
    return render_template('members/search_member.html')