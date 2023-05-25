from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db, ma
from src.models.housing import Housing
from src.models.publication import Publication
from src.models.comment import Comment
from src.roles_and_categories import Roluser
from sqlalchemy.orm import validates
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False,unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    dateBirth = db.Column(db.Date,nullable=False)
    rol_user = db.Column(db.Enum(Roluser),default=Roluser.landlord)
    housings = db.relationship('Housing', backref="owner")
    publications = db.relationship('Publication', backref="owner")
    comments = db.relationship('Comment', backref="owner")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self,**fields):#Constructor, reciben muchos parametros
        super().__init__(**fields)
    
    def __repr__(self) -> str:#Similar a toString()
        return f"User >>> {self.name}"
    
    def __setattr__(self, name, value):
        if(name == "password"):
            value = User.hash_password(value)
        super(User, self).__setattr__(name, value)
        
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_user, password)
    
    @staticmethod
    def hash_password(password_user):
        if not password_user:
            raise AssertionError('Password not provided')
        if not re.match('\d.*[A-Z]|[A-Z].*\d', password_user):
            raise AssertionError('Password must contain 1 capital letter and 1 number')
        if len(password_user) < 7 or len(password_user) > 20:
            raise AssertionError('Password must be between 7 and 20 characters')
        
        return generate_password_hash(password_user)
    
    @validates(id)
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if User.query.filter(User.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates(name_user)
    def validate_name_user(self,key,value):
        if not value:
            raise AssertionError('No name provided')
        if not value.isalnum():
            raise AssertionError('Name value must be alphanumeric')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('Name user must be between 5 and 50 characters')

        return value 
    
    @validates(email)
    def validate_email(self,key,value):
        if not value:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise AssertionError('Provided email is not an email address')
        if User.query.filter(User.email == value).first():
            raise AssertionError('Email is already in use')
        
        return value
    
    @validates(phone)
    def validate_phone(self,key,value):
        if not value:
            raise AssertionError('No phone')
        if not value.isalnum():
            raise AssertionError('Phone value must be alphanumeric')
        if len(value) < 10 or len(value) > 10:
            raise AssertionError('Phone must be 10 characters')

        return value
    
    @validates(dateBirth)
    def validate_dateBirth(self,key,value):
        # This field is not mandatory!
        if not value:
            raise value
        if not re.match("[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}", value):
            raise AssertionError('Provided date is not a real date value')
        today = datetime.datetime.now()
        dateBirth = datetime.datetime.strptime(value, "%Y-%m-%d")
        if not dateBirth < today:
            raise AssertionError('date birth invalid')
        return value
    
    @validates(rol_user)
    def validate_rol_user(self, key, value):
        allowed_values = [1, 2, 3]
        if not value:
            raise AssertionError('No rol user')
        if value not in allowed_values:
            raise ValueError('El valor del campo "rol_user" no es válido. Los valores permitidos son 1, 2 y 3.')
        return value
        
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)