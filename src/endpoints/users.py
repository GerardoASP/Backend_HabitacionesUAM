from flask import Blueprint,request
users = Blueprint("users",__name__,url_prefix="/api/v1/users")
from http import HTTPStatus

# Data for example purposes
product_data = [
 {"id": 1, "nameUser": "Papitas", "password": "1000", "rolUser": "Admin",},
 {"id": 2, "nameUser": "Romulo", "password": "2000", "rolUser": "Lesse"},
 {"id": 3, "nameUser": "Fruco", "password": "3000", "rolUser": "Lesse"},
 {"id": 4, "nameUser": "Yuna", "password": "4000", "rolUser": "Student-Parent"},
 {"id": 5, "nameUser": "Gar", "password": "5000", "rolUser": "Student-Parent"},
];

@users.get("/")
def read_all():
    return {"data": product_data}, HTTPStatus.OK
@users.get("/<int:id>")
def read_one(id):
    for product in product_data:
      if product['id'] == id:
        return {"data": product}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@users.post("/")
def create():
    post_data = request.get_json()
 
    product = {
        "id": len(product_data) + 1, 
        "nameUser": post_data.get('nameUser', 'No Name'), 
        "password": post_data.get('password', None), 
        "rolUser": post_data.get('rolUser', None)
    }
 
    product_data.append(product)
 
    return {"data": product}, HTTPStatus.CREATED

@users.put('/<int:id>')
@users.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(product_data)):
      if product_data[i]['id'] == id:
        product_data[i] = {
            "id": id,
            "nameUser": post_data.get('nameUser'), 
            "password": post_data.get('password'), 
            "rolUser": post_data.get('rolUser')
        }
        return {"data": product_data[i]}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@users.delete("/<int:id>")
def delete(id):
    for i in range(len(product_data)):
        if product_data[i]['id'] == id:
            del product_data[i]
            return {"data": ""}, HTTPStatus.NO_CONTENT
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND