from flask import Blueprint,request
housings = Blueprint("housings",__name__,url_prefix="/api/v1/housings")
from http import HTTPStatus

product_data = [
 {"id": 1, "state": "Available", "categoryHou": 1, "stratum": "3","value":340000,"description":"","altitude":"37.7749° N","latitude":"122.4194° O","fkidUser":None},
 {"id": 2, "state": "Available", "categoryHou": 2, "stratum": "3","value":350000,"description":"","altitude":"36.7749° N","latitude":"132.4194° O","fkidUser":None},
 {"id": 3, "state": "Available", "categoryHou": 3, "stratum": "3","value":300000,"description":"","altitude":"47.7749° N","latitude":"112.4194° O","fkidUser":None},
 {"id": 4, "state": "Not available", "categoryHou": 4, "stratum": "2","value":230000,"description":"","altitude":"37.7748° N","latitude":"100.4194° O","fkidUser":None},
 {"id": 5, "state": "Not available", "categoryHou": 1, "stratum": "2","value":250000,"description":"","altitude":"32.7749° N","latitude":"22.4194° O","fkidUser":None},
];

@housings.get("/")
def read_all():
    return {"data": product_data}, HTTPStatus.OK

@housings.get("/")
def read_available_housings():
    query_state = request.args.get('state')

@housings.get("/")
def read_lesse_user_housings():
    query_fore_key = request.args.get('fk_idUser')
    query_rol = request.args.get('rolUser')
    
@housings.get("/<int:id>")
def read_one(id):
    for product in product_data:
      if product['id'] == id:
        return {"data": product}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@housings.post("/")
def create():
    post_data = request.get_json()
 
    product = {
        "id": len(product_data) + 1, 
        "state": post_data.get('state', 'Available'), 
        "categoryHou": post_data.get('categoryHou', None), 
        "stratum": post_data.get('stratum', None),
        "value": post_data.get('value',0),
        "description": post_data.get('description',None),
        "altitude": post_data.get('altitude',None),
        "latitude": post_data.get('latitude',None),
        "fkidUser": post_data.get('fkidUser',None),
    }
 
    product_data.append(product)
 
    return {"data": product}, HTTPStatus.CREATED
@housings.put('/<int:id>')
@housings.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(product_data)):
      if product_data[i]['id'] == id:
        product_data[i] = {
            "id": id,
            "state": post_data.get('state'), 
            "categoryHou": post_data.get('categoryHou'), 
            "stratum": post_data.get('stratum'),
            "value": post_data.get('value'),
            "description": post_data.get('description'),
            "altitude": post_data.get('altitude'),
            "latitude": post_data.get('latitude')
        }
        return {"data": product_data[i]}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@housings.delete("/<int:id>")
def delete(id):
    for i in range(len(product_data)):
        if product_data[i]['id'] == id:
            del product_data[i]
            return {"data": ""}, HTTPStatus.NO_CONTENT
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

