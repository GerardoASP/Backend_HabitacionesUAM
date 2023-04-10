from flask import Blueprint,request
users = Blueprint("users",__name__,url_prefix="/api/v1/users")

@users.get("/")
def read_all():
    return "Reading al users ... soon"
@users.get("/<int:id>")
def read_one(id):
    return "Reading a user ... soon"
@users.post("/")
def create():
    return "Creating a user ... soon"
@users.put('/<int:id>')
@users.patch('/<int:id>')
def update(id):
    return "Updating a user ... soon"
@users.delete("/<int:id>")
def delete(id):
    return "Removing a user ... soon"