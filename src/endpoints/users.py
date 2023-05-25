from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from datetime import datetime
from src.database import db
from src.models.user import User, user_schema, users_schema

users = Blueprint("users",__name__,url_prefix="/api/v1/users")

@users.get("/")
def read_all():
    users = User.query.order_by(User.name_user).all() 
    return {"data": users_schema.dump(users)}, HTTPStatus.OK

@users.get("/<int:id>")
def read_one(id):
    user = User.query.filter_by(id=id).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    date_birth_request = request.get_json().get("dateBirth", None)
    date_birth = datetime.strptime(date_birth_request, '%Y-%m-%d').date()
    # User.id is auto increment! 
    user = User(name_user = request.get_json().get("name_user", None),
        password = request.get_json().get("password", None),
        email = request.get_json().get("email", None),
        phone = request.get_json().get("phone", None),
        dateBirth = date_birth,
        rol_user = request.get_json().get("rol_user", None))

    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": user_schema.dump(user)}, HTTPStatus.CREATED

@users.put('/<int:id>')
@users.patch('/<int:id>')
def update(id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    user = User.query.filter_by(id=id).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    date_birth_request = request.get_json().get("dateBirth", None)
    date_birth = datetime.strptime(date_birth_request, '%Y-%m-%d').date()
    
    user.name_user = request.get_json().get('name_user', user.name_user)
    user.password = request.get_json().get('password', user.password)
    user.email = request.get_json().get('email', user.email)
    user.phone = request.get_json().get('phone', user.phone)
    user.dateBirth =  date_birth
    user.rol_user = request.get_json().get('rol_user', user.rol_user)
    
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.delete("/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": ""}, HTTPStatus.NO_CONTENT