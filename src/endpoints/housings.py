from flask import Blueprint, request,abort
from http import HTTPStatus
import sqlalchemy.exc
import werkzeug
from datetime import datetime
from src.database import db
from src.models.housing import Housing,housing_schema,housings_schema

housings = Blueprint("housings",__name__,url_prefix="/api/v1/housings")

@housings.get("/")
def read_all():
    housings = Housing.query.order_by(Housing.description).all() 
    return {"data": housings_schema.dump(housings)}, HTTPStatus.OK

@housings.get("/available")
def read_available_housings():
    housings = Housing.query.filter_by(state="available").order_by(Housing.description).all()
    return {"data": housings_schema.dump(housings)}, HTTPStatus.OK

@housings.get("/not_available")
def read_not_available_housings():
    housings = Housing.query.filter_by(state="not available").order_by(Housing.description).all()
    return {"data": housings_schema.dump(housings)}, HTTPStatus.OK


@housings.get("/<int:id>")
def read_one(id):
    housing = Housing.query.filter_by(id=id).first()
    if(not housing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": housing_schema.dump(housing)}, HTTPStatus.OK

@housings.get("/user/<int:landlord_id>")
def read_one_two(landlord_id):
    
    housing = Housing.query.filter_by(landlord_id=landlord_id).all()

    if (not housing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data": housings_schema.dump(housing)}, HTTPStatus.OK


@housings.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    # Housing.id is auto increment! 
    housing = Housing(stratum = request.get_json().get("stratum", None),
        description = request.get_json().get("description", None),
        state = request.get_json().get("state", None),
        value = request.get_json().get("value", None),
        latitude = request.get_json().get("latitude", None),
        altitude = request.get_json().get("altitude", None),
        video = request.get_json().get("video", None),
        landlord_id = request.get_json().get("landlord_id", None),
        lessee_id = request.get_json().get("lessee_id", None))

    try:
        db.session.add(housing)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": housing_schema.dump(housing)}, HTTPStatus.CREATED

@housings.put('/<int:id>')
@housings.patch('/<int:id>')
def update(id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Put body JSON data not found","message": str(e)}, HTTPStatus.BAD_REQUEST
    housing = Housing.query.filter_by(id=id).first()
    if(not housing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    housing.stratum = request.get_json().get("stratum", housing.stratum)
    housing.description = request.get_json().get("description", housing.description)
    housing.state = request.get_json().get("state", housing.state)
    housing.value = request.get_json().get("value", housing.value)
    housing.latitude = request.get_json().get("latitude", housing.latitude)
    housing.altitude = request.get_json().get("altitude", housing.altitude)
    housing.video = request.get_json().get("video", housing.video)
    housing.landlord_id = request.get_json().get("landlord_id", housing.landlord_id)
    housing.lessee_id = request.get_json().get("lessee_id", housing.lessee_id)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": housing_schema.dump(housing)}, HTTPStatus.OK

@housings.delete("/<int:id>")
def delete(id):
    housing = Housing.query.filter_by(id=id).first()
    if(not housing):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(housing)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Resource could not be deleted","message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"data": ""}, HTTPStatus.NO_CONTENT



