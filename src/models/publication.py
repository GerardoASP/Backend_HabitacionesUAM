from datetime import datetime
from src.database import db, ma
from src.models.comment import Comment
from src.models.user import User
from sqlalchemy.orm import validates
import re

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    datePublication = db.Column(db.Date,nullable=False)
    state = db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text, nullable=False, unique=True)
    punctuation = db.Column(db.Integer,nullable=False)
    comments = db.relationship('Comment', backref="owner")
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Publication >>> {self.content}"
    
    @validates(id)
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if Publication.query.filter(Publication.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates(datePublication)
    def validate_dateBirth(self,key,value):
        # This field is not mandatory!
        if not value:
            raise value
        if not re.match("[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}", value):
            raise AssertionError('Provided date is not a real date value')
        today = datetime.datetime.now()
        datePublication = datetime.datetime.strptime(value, "%Y-%m-%d")
        if not datePublication >= today:
            raise AssertionError('Date publication must be today or later')
        return value
    
    @validates(content)
    def validate_content(self,key,value):
        if not value:
            raise AssertionError('No concept provided')
        if len(value) < 5 or len(value) > 50:
            raise AssertionError('content must be between 5 and 50 characters')
        if value.isdigit():
            raise AssertionError('content invalid')
        return value
    
    @validates(punctuation)
    def validate_punctuation(self, key, value):
        if not value:
            raise AssertionError('No punctuation provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        return value
    
    @validates(state)
    def validate_state(self, key, value):
        allowed_values = ["available", "not available"]
        if not value:
            raise AssertionError('No state provided')
        if value not in allowed_values:
            raise ValueError('The value state is not valid. The allowed values are "available" and "not available".')
        return value
    
    @validates(user_id)
    def validate_user_id(self, key, value):
        user = User.query.get(value)
        if not value:
            raise value
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('user_id invalid')
        if not user:
            raise AssertionError('user_id does not exist')
        return value
        

class PublicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Publication
        include_fk = True

publication_schema = Publication()
publications_schema = Publication(many=True)