from flask import Blueprint,request,jsonify, render_template
from service.ticket_service import TicketService

ticket_bp=Blueprint('ticket_bp',__name__)
service=TicketService()

@ticket_bp.route('/tickets',methods=['POST'])
def create():

    data=request.get_json()

    service.create_ticket(
    data['title'],
    data['description'],
    data['status'],
    data['priority'],
    data.get('assigned_to'),
    data.get('due_date')
    )

    return jsonify({"message":"Created"})

@ticket_bp.route('/tickets',methods=['GET'])
def fetch():

    tickets=service.fetch_all()

    return jsonify([t.__dict__ for t in tickets])

@ticket_bp.route('/tickets/<int:id>',methods=['PUT'])
def update(id):

    data=request.get_json()

    service.update_ticket(
    id,
    data['title'],
    data['description'],
    data['status'],
    data['priority'],
    data.get('assigned_to'),
    data.get('due_date')
    )

    return jsonify({"message":"Updated"})

@ticket_bp.route('/tickets/<int:id>',methods=['DELETE'])
def delete(id):

    service.delete(id)

    return jsonify({"message":"Deleted"})

@ticket_bp.route('/tickets/status/<status>')
def status(status):

    tickets=service.fetch_by_status(status)

    return jsonify([t.__dict__ for t in tickets])

@ticket_bp.route('/search/<title>')
def search(title):

    tickets=service.search(title)

    return jsonify([t.__dict__ for t in tickets])

@ticket_bp.route('/dashboard')
def dashboard():

    return jsonify(service.dashboard())
@ticket_bp.route('/dashboard')
def dashboard_page():
    return render_template("index.html")