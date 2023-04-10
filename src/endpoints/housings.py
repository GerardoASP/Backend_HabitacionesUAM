from flask import Blueprint,request
housings = Blueprint("housings",__name__,url_prefix="/api/v1/housings")

@housings.get("/")
def read_all():
    return "Reading al housings ... soon"

@housings.get("/")
def read_housings_of_category():
    name_category = request.args.get('categoryHou')

@housings.get("/")
def read_available_housings():
    query_state = request.args.get('state')

@housings.get("/")
def read_lesse_user_housings():
    query_fore_key = request.args.get('fk_idUser')
    query_rol = request.args.get('rolUser')
@housings.get("/<int:id>")
def read_one(id):
    return "Reading a housing ... soon"
@housings.post("/")
def create():
    return "Creating a housing ... soon"
@housings.put('/<int:id>')
@housings.patch('/<int:id>')
def update(id):
    return "Updating a housing ... soon"
@housings.delete("/<int:id>")
def delete(id):
    return "Removing a housing ... soon"

