from flask import Blueprint,request
comments = Blueprint("comments",__name__,url_prefix="/api/v1/comments")
from http import HTTPStatus

@comments.get("/")
def read_all():
    return "Reading al comments ... soon"

@comments.get("/<int:id>")
def read_one(id):
    return "Reading a comment ... soon"
@comments.post("/")
def create():
    return "Creating a comment ... soon"
@comments.put('/<int:id>')
@comments.patch('/<int:id>')
def update(id):
    return "Updating a comment ... soon"
@comments.delete("/<int:id>")
def delete(id):
    return "Removing a comment ... soon"