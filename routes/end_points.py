from flask_restful import Api
from routes.views import Login, Signup, Resetpass,Taskcreate,Tasklist,Userlist

def generate_routes(app):
    api=Api(app)
    api.add_resource(Login,'/login')
    api.add_resource(Signup,'/register')
    api.add_resource(Resetpass,'/reset')
    api.add_resource(Taskcreate,'/create')
    api.add_resource(Tasklist, '/tlist')
    api.add_resource(Userlist, '/ulist')
    return api

