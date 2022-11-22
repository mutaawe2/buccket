from bucketList.models import Bucketitems
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse 
import datetime 
from bucketList.schema.app_schema import bucketListSchema

bucket_list = bucketListSchema()
bucket_items = bucketListSchema(many=True)


class Buck(Resource):
    """This class handles GET, PUT, DELETE requests."""
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        
    # post method for creating a new bucketlist
    # route = /api/bucketlists
    @jwt_required
    def post(self):
        self.parser.add_argument('name', type=str, required=True, help='Name cannot be blank!')
        self.parser.add_argument('description', type=str, required=True, help='Description cannot be blank!')
        self.parser.add_argument('completed', type=bool, required=False , help='Completed cannot be blank!')
        user_id = get_jwt_identity()
        
        data = self.parser.parse_args()
        
        bucketlist = Bucketitems(**data ,created_by=user_id['id'] ,due_date=datetime.datetime.now())
        bucketlist.save()
        
        
        return {'message': 'Bucketlist created successfully'}, 201
        
    # get method for getting all bucketlists
    @jwt_required
    def get_bucketlist(self , bucketlist_id = None):
        # check if the user is logged in
        if bucketlist_id:
            bucketlist = Bucketitems.get_by_id(bucketlist_id)
            if bucketlist:
                return bucket_list.dump(bucketlist)
            return {'message': 'Bucketlist not found'}, 404
        
        user_id = get_jwt_identity()
        bucketlists = Bucketitems.get_all(user_id)
        return bucket_items.dump(bucketlists)
        
    # get method for getting a single bucketlist
    @jwt_required
    def get_bucketlist_item(self, id):
        if get_jwt_identity():
            user_id = get_jwt_identity()
            bucketlist = Bucketitems.get_by_id(id)
            if bucketlist:
                if bucketlist.created_by == user_id['id']:
                    return {'bucketlist': bucketlist.serialize()}, 200
                return {'message': 'You are not authorized to view this bucketlist!'}, 401
            return {'message': 'Bucketlist not found!'}, 404
        
    # put method for updating a bucketlist where all fields are optional 
    @jwt_required
    def update_bucketlist(self, bucketlist_id):
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('completed', type=bool)
        
        bucket_list = bucket_items.get_by_id(bucketlist_id)
        
        if not bucket_list:
            return {'message': 'Bucketlist not found!'}, 404
        
        # check ownership
        if bucket_list.created_by != get_jwt_identity():
            return {'message': 'You are not authorized to update this bucketlist!'}, 401
        
        data = self.parser.parse_args()
        
        # update bucketlist if there is new data
        Bucketitems.name = data['name'] if data['name'] else bucket_list.name
        Bucketitems.description = data['description'] if data['description'] else bucket_list.description
        Bucketitems.completed = data['completed'] if data['completed'] else bucket_list.completed
        Bucketitems.due_date = datetime.datetime.now()
        Bucketitems.update()
        
        # return Updated Bucketitems 
        return Bucketitems.dump(bucket_list), 200
    
    # delete method for deleting a bucketlist
    @jwt_required
    def delete_bucketlist(self, bucketlist_id):
        bucket_list = Bucketitems.get_by_id(bucketlist_id)
        
        if not bucket_list:
            return {'message': 'Bucketlist not found!'}, 404
        
        # check ownership
        if bucket_list.created_by != get_jwt_identity():
            return {'message': 'You are not authorized to delete this bucketlist!'}, 401
        
        bucket_list.delete()
        
        return {'message': 'Bucketlist deleted successfully!'}, 200
        
        
        