from bucketList.user.bucket_user import Users

def user_routes(api):
    api.add_resource(Users, '/api/users')