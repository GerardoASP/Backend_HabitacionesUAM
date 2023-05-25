from datetime import datetime
from src.database import db, ma
from src.models.user import User
from sqlalchemy.orm import validates
import re

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    dateComment = db.Column(db.Date,nullable=False)
    content = db.Column(db.Text, nullable=False, unique=True)
    state = db.Column(db.String(50),nullable=False)
    publication_id = db.Column(db.Integer,db.ForeignKey('publication.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __init__(self, **fields):
        super().__init__(**fields)
    
    def __repr__(self) -> str:
        return f"Comment >>> {self.description}"
    
    @validates(id)
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not re.compile("^[-+]?[0-9]+$", value):
            raise AssertionError('The value must be an integer')
        if value <= 0:
            raise AssertionError('id invalid')
        if Comment.query.filter(Comment.id == value).first():
            raise AssertionError('Id is already in use') 
        
        return value
    
    @validates(dateComment)
    def validate_dateBirth(self,key,value):
        # This field is not mandatory!
        if not value:
            raise value
        if not re.match("[0-9]{1,2}\\-[0-9]{1,2}\\-[0-9]{4}", value):
            raise AssertionError('Provided date is not a real date value')
        today = datetime.datetime.now()
        datePublication = datetime.datetime.strptime(value, "%Y-%m-%d")
        if not datePublication >= today:
            raise AssertionError('Date comment must be today or later')
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
    
    
class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Comment
        include_fk = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)