from flask import Flask
from config.db_inti import db
from config.db_file import sql_config
from routes.end_points import generate_routes

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_config
    app.config['DEBUG']=True

    with app.app_context():
        generate_routes(app)
        db.init_app(app)
        db.create_all()
    return app

if __name__=="__main__":
    app=create_app()
    app.run(port=3030,debug=True)

