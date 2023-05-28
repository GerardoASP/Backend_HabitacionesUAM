from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db, ma
from src.models.housing import Housing
from src.models.publication import Publication
from src.models.comment import Comment

from sqlalchemy.orm import validates
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False,unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    dateBirth = db.Column(db.Date,nullable=False)
    rol_user = db.Column(db.Integer,nullable=False)
    #housings = db.relationship('Housing', backref="owner")
    #housings = db.relationship('Housing', backref="owner", foreign_keys=['Housing.landlord_id', 'Housing.lessee_id'])
    #housings = db.relationship('Housing', backref="owner", foreign_keys=[Housing.landlord_id, Housing.lessee_id])
    housings = db.relationship('Housing', backref="owner", primaryjoin="or_(User.id == Housing.landlord_id, User.id == Housing.lessee_id)")
    #publications = db.relationship('Publication', backref="owner")
    #comments = db.relationship('Comment', backref="owner")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self,**fields):#Constructor, reciben muchos parametros
        super().__init__(**fields)
    
    def __repr__(self) -> str:#Similar a toString()
        return f"User >>> {self.name_user}"
    
    def __setattr__(self, name, value):
        if(name == "password"):
            value = User.hash_password(value)
        super(User, self).__setattr__(name, value)
        
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def hash_password(password):
        if not password:
            raise AssertionError('Password not provided')
        if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError('Password must contain 1 capital letter and 1 number')
        if len(password) < 7 or len(password) > 20:
            raise AssertionError('Password must be between 7 and 20 characters')
        
        return generate_password_hash(password)
    
    @validates('id')
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
    
    @validates('name_user')
    def validate_name_user(self,key,value):
        if not value:
            raise AssertionError('No name provided')
        if not value.isalnum():
            raise AssertionError('Name value must be alphanumeric')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('Name user must be between 5 and 50 characters')

        return value 
    
    @validates('email')
    def validate_email(self,key,value):
        if not value:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise AssertionError('Provided email is not an email address')
        if User.query.filter(User.email == value).first():
            raise AssertionError('Email is already in use')    
        return value
    
    @validates('phone')
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
    
    @validates('rol_user')
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

#Error
# File "C:\Users\GERARDO SANCHEZ\Desktop\Programacion_Backend
# \backend\proyecto_habitaciones_uam_v1\venv\Lib\site-packages\
#  sqlalchemy\orm\relationships.py", line 2467, in _determine_joins
#    raise sa_exc.AmbiguousForeignKeysError(
#sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join 
#condition between parent/child tables on relationship User.housings - 
#there are multiple foreign key paths linking the tables.  Specify the 
#'foreign_keys' argument, providing a list of those columns which should 
#be counted as containing a foreign key reference to the parent table.



#Posible Solución
#Cambiar el formato de la linea housings = db.relationship('Housing', backref="owner")
#por el siguiente formato:housings = db.relationship('Housing', backref='owner', foreign_keys=['Housing.landlord_id', 'Housing.lessee_id'])
#No Funciono

#Solucion
#housings = db.relationship('Housing', backref="owner", primaryjoin="or_(User.id == Housing.landlord_id, User.id == Housing.lessee_id)")

#Error
#File "C:\Users\GERARDO SANCHEZ\Desktop\Programacion_Backend\backend\
    # proyecto_habitaciones_uam_v1\venv\Lib\site-packages\
        # sqlalchemy\sql\coercions.py", line 535, 
        # in _raise_for_expected
    #raise exc.ArgumentError(msg, code=code) from err
#sqlalchemy.exc.ArgumentError: Column expression expected for argument 'foreign_keys'; got 'Housing.lessee_id'.

#Posible Solución
#housings = db.relationship('Housing', backref="owner", foreign_keys=[Housing.landlord_id, Housing.lessee_id])

#Error
#raise LookupError(
#sqlalchemy.exc.StatementError: (builtins.LookupError) '1' is not among the defined enum values. Enum name: roluser. Possible values: admin, landlord, less
#[SQL: INSERT INTO user (name_user, password, email, phone, "dateBirth", rol_user, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)]
#[parameters: [{'email': 'gery@autonoma.edu.co', 'password': 'pbkdf2:sha256:260000$ppeSVofQ1gTFOQnS$72f2bf344e5ae6b2895ee7a0fa6cd11f3f6b781b83b8d3db3c58661a66178f02', 'rol_user': 1, 'phone': '3004966437', 'dateBirth': datetime.date(2000, 5, 18), 'name_user': 'geryy', 'updated_at': None}]]


