from config.db_inti import db
import datetime
from flask_bcrypt import Bcrypt

bcr=Bcrypt()

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    email= db.Column(db.String(40),nullable=True)
    password=db.Column(db.String(12),nullable=True)
    task=db.relationship('Task',backref='acess',lazy=True)
    @property
    def passprase(self):
        return self.password

    @passprase.setter
    def passprase(self,pawd):
        self.password=bcr.generate_password_hash(pawd).decode('utf-8')

    def to_dict(self):
        return {
            # 'id':self.id,
            'name':self.name,
            'email':self.email,
            'password':self.password
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name= db.Column(db.String(125), nullable=True)
    date_created= db.Column(db.DateTime, nullable=True,default=datetime.date.today())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)

    def to_dict(self):
        task_dict= {'id':self.id,
                'task_name':self.task_name,
                'date_created':self.date_created.strftime('%Y-%m-%d') if self.date_created else None}
        if self.status is not None:
            task_dict['staus']=self.status.status
        else:
            task_dict['staus']="Not provided"
        return task_dict


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status=db.Column(db.String(20),nullable=True)
    stat=db.relationship('Task',backref='status',lazy=True)


