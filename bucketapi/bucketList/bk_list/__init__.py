from bucketList.bk_list.items import Buck as items 

def bucket_routes(api):
    api.add_resource(items, '/api/bucketlists', '/api/bucketlists/<int:id>')