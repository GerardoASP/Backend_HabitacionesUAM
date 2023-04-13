from flask import Blueprint,request
publications = Blueprint("publications",__name__,url_prefix="/api/v1/publications")
from http import HTTPStatus

@publications.get("/")
def read_all():
    return "Reading al publications ... soon"
@publications.get("/<int:id>")
def read_one(id):
    return "Reading a publication ... soon"
@publications.post("/")
def create():
    return "Creating a publication ... soon"
@publications.put('/<int:id>')
@publications.patch('/<int:id>')
def update(id):
    return "Updating a publication ... soon"
@publications.delete("/<int:id>")
def delete(id):
    return "Removing a publication ... soon"