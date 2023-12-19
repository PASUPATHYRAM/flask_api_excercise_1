from flask_restful import Resource
from table.tables import User,Task
from table.Schemas import User_schema,Task_schema
from flask import request
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from table.validator import User_form,Task_form,Status_form
from config.db_inti import db
from datetime import datetime

from loggers.log_records import Logcreator

bcr=Bcrypt()

class Login(Resource):
    def __init__(self):
        pass

    def post(self):
        data=request.get_json()
        if not 'name' in data and not 'password' in data:
            return {"message":"Need username/email and password"}

        name=data.get('name').strip()
        password=data.get('password').strip()
        if not name and not password:
            return {"message":"name and password shouldnt none"}
        user=self.user_query(name)
        log=Logcreator()

        if user and bcr.check_password_hash(user.password,password):
            log.message("Logged in succesful")
            return {"message:":"you {} sucessfully logged in ".format(user.name)}
        else:
            log.message("Logged in unsuccesful - passwords dont match")
            return {"message":"Incorrect password"}



    @staticmethod
    def user_query(name):
        user=User.query.filter(or_(User.name==name, User.email==name)).first()
        return user


class Signup(Resource):
    def __init__(self):
        pass

    def post(self):
        data=request.get_json()
        vali=User_form(data=data)
        log=Logcreator()
        sc=User_schema()
        if not vali.validate():
            log.message("Validation Failed")
            return {"message":"validation error","errors":vali.errors}
        new_user=User()
        new_user.name=data.get('name').strip()
        new_user.email=data.get('email').strip()
        new_user.passprase=data.get('password').strip()
        errors=sc.validate(new_user.to_dict())
        if errors:
            log.message("Schema error-")
            return {"message":"Schemaerros","errors":errors}
        db.session.add(new_user)
        db.session.commit()
        log.message("User_added")
        return {'Message:': 'User added'}

class Resetpass(Login):
    def __init__(self):
        pass
    def patch(self):
        data=request.get_json()
        name=data.get('name').strip()
        new_pass=data.get('newpassword').strip()
        if not name in data and not new_pass in data:
            return {"message":"Need name and new_pass field"}
        user=self.user_query(name)
        if not user:
            return {"message":"User details not found"}
        user.passprase=new_pass
        db.session.commit()
        return {"message:":"Password changed"}


class Taskcreate(Login):
    def __init__(self):
        pass
    def post(self):
        data=request.get_json()
        log = Logcreator()
        vali=Task_form(data=data)

        if not vali.validate():
            log.message(vali.errors)
            return {'error':vali.errors}
        task_name=data.get('task_name').strip()
        date_created=datetime.strptime(data.get('date_created').strip(), '%m-%Y-%d')
        name=data.get('name').strip()
        user=self.user_query(name)
        if not user:
            return {'Message':"User not found"}
        task=Task()
        task.user_id=user.id
        task.task_name=task_name
        task.date_created=date_created
        task_sc=Task_schema()
        err=task_sc.validate(task.to_dict())
        if err:
            log.message(err)
        db.session.add(task)
        db.session.commit()
        return {'message':'Task added'}

    def get(self):
        users = User.query.all()# Query all users
        user_list = []
        for user in users:
            user_dict = user.to_dict()  # Get user details
            user_dict['tasks'] = []  # Initialize tasks list
            for task in user.task:  # Loop through user's tasks
                task_dict = task.to_dict()  # Get task details
                user_dict['tasks'].append(task_dict)  # Add task to user's tasks list
            user_list.append(user_dict)  # Add user to user list
        return {'users': user_list}  # Return list of users

class Tasklist(Resource):
    def __init__(self):
        pass

    def get(self):
        task=Task.query.all()
        task_list=[]
        for ta in task:
            task_list.append(ta.to_dict())
        return {"task_list":task_list}

class Userlist(Resource):
    def __init__(self):
        pass

    def get(self):
        limit=request.args.get('limit',default=5,type=int)
        try:
            user=User.query.all()
            emp=[]
            for u in user:
                a=u.to_dict1()
                emp.append(a)
            return {'Userlist': emp[:limit]}

            # return {'User_list':[users.to_dict1() for users in user]}
        except Exception as e:
            return {'message':str(e)}











