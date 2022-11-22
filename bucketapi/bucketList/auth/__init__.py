from bucketList.auth.resource import login, register, logout

def auth_routes(api):
    api.add_resource(login, '/api/login')
    api.add_resource(register, '/api/register')
    api.add_resource(logout, '/api/logout')