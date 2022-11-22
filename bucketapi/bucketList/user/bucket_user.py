from bucketList.models import User
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from bucketList.schema.app_schema import UserSchema

class Users(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        
    @jwt_required
    def get(self , user_id=None):
        if user_id:
            if not user_id == get_jwt_identity()['id']:
                return {'message': 'You are not authorized to view this page!'}, 401
            
            # get single user 
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return {'message': 'User not found!'}, 404
            
            return UserSchema.dump(user).data, 200
        
        # get all users 
        users = User.query.all()
        return UserSchema.dump(users, many=True).data, 200