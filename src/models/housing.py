from datetime import datetime
from src.database import db, ma
from src.models.user import User
from sqlalchemy.orm import validates
import re

class Housing(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    stratum = db.Column(db.Integer,nullable=False)
    description = db.Column(db.Text, nullable=False, unique=True)
    state = db.Column(db.String(50),nullable=False)
    value = db.Column(db.Float,nullable=False)
    latitude = db.Column(db.Float,nullable=False)
    altitude = db.Column(db.Float,nullable=False)
    video = db.Column(db.String(50),nullable=True)
    landlord_id = db.Column(db.Integer,db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    lessee_id = db.Column(db.Integer,db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Housing >>> {self.description}"
    
    @validates(id)
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if Housing.query.filter(Housing.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates(description)
    def validate_content(self,key,value):
        if not value:
            raise AssertionError('No description provided')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('description must be between 5 and 50 characters')
        if value.isdigit():
            raise AssertionError('description invalid')
        return value
    
    @validates(state)
    def validate_state(self, key, value):
        allowed_values = ["available", "not available"]
        if not value:
            raise AssertionError('No state provided')
        if value not in allowed_values:
            raise ValueError('The value state is not valid. The allowed values are "available" and "not available".')
        return value
    
    @validates(value)
    def validate_value(self, key, value):
        if not value:
            raise AssertionError('No value provided')
        if not isinstance(value, (float)):
            raise AssertionError('The value must be float')
        if value <= 0:
            raise AssertionError('value invalid')
        return value
    
    @validates(latitude)
    def validate_latitude(self, key, value):
        if not value:
            raise AssertionError('No latitude provided')
        if value <= 0:
            raise AssertionError('latitude invalid')
        if not isinstance(value, (float)):
            raise AssertionError('The value must be float')
        return value
    
    @validates(altitude)
    def validate_altitude(self, key, value):
        if not value:
            raise AssertionError('No altitude provided')
        if value <= 0:
            raise AssertionError('altitude invalid')
        if not isinstance(value, (float)):
            raise AssertionError('The value must be float')
        return value
    
    @validates(landlord_id)
    def validate_landlord_id(self, key, value):
        user = User.query.get(value)
        if not value:
            raise AssertionError('No fk_landlord_id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('fk_landlord_id invalid')
        if not user:
            raise AssertionError('fk_landlord_id does not exist')
        return value
    
    @validates(lessee_id)
    def validate_lessee_id(self, key, value):
        user = User.query.get(value)
        if not value:
            raise value
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('lessee_id invalid')
        if not user:
            raise AssertionError('lessee_id does not exist')
        return value
    
    @validates(stratum)
    def validate_stratum(self, key, value):
        if not value:
            raise AssertionError('No stratum provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('stratum invalid')
        return value

class HousingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Housing
        include_fk = True

housing_schema = HousingSchema()
housings_schema = HousingSchema(many=True)