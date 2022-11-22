from bucketList.models import Bucketitems 
from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema


class UserSchema(Schema):
    class Meta:
        feilds = ('id', 'name', 'email')
        
class bucketListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bucketitems
        include_fk = True