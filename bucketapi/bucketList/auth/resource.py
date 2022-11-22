from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity ,
    jwt_required,
)
from bucketList.models import User


# login class for logging in a user
class login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('email', type=str, required=True, help='Email cannot be blank!')
        self.parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')
        data = self.parser.parse_args()

        user = User.get_by_email(data['email'])
        if user and user.verify_password(data['password'] , user.password):
            identity = {'id': user.id, 'email': user.email}
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)
            return {
                    'message': 'Logged in as {}'.format(user.email),
                    'access_token': access_token,
                    'refresh_token': refresh_token
            }, 200
        return {'message': 'Wrong credentials!'}, 401
        
    
# register a user 
class register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('username', type=str, required=True, help='Username cannot be blank!')
        self.parser.add_argument('email', type=str, required=True, help='Email cannot be blank!')
        self.parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')
        data = self.parser.parse_args()

        if User.get_by_email(data['email']):
            return {'message': 'User already exists!'}, 409

        new_user = User(
            name = data['username'],
            email = data['email'], 
            password = User.hash_password(data['password'])
        )
        new_user.save()
        return {'message': 'User created successfully!'}, 201
    
    
# log out the user 
class logout(Resource):
    @jwt_required
    def post(self):
        user_logout = get_jwt_identity()
        if user_logout:
            return {'message': 'Successfully logged out!'}, 200
        return {'message': 'Something went wrong!'}, 500