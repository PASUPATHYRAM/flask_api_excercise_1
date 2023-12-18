from wtforms import Form,Field,ValidationError,validators,StringField
from wtforms.validators import Length,Email
from wtforms.meta import DefaultMeta
import re

def email_validator(form,field):
    email=field.data
    if '@' in email:
        return True
    raise ValidationError("Invlaid email")

def pass_valid(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Should have at least 1 capital letter")
    if not re.search(r'\d', password):
        raise ValidationError("Should contain at least 1 number")
    if not re.search(r'[!@#]', password):
        raise ValidationError("Should contain any of this character @,#,!")

def task_name_checker(form,field):
    task_name=field.data
    if not re.search(r'[-]',task_name):
        raise ValidationError("Separator missing. add '-' ")

def date_checker(form,field):
    date=field.data
    if re.match(r'\d{2}-\d{4}-\d{2}',date):
        month,year,day=map(int,date.split('-'))
        if month>13:
            raise ValidationError("Month should not greater than 12")
    else:
        raise ValidationError("Date format should be MM-YYYY-DD")


def status_check(form,field):
    stat=field.data
    if not str(stat).upper() in ['WIP',"DONE","YET TO START"]:
        raise ValidationError("Incorrect status")



class User_form(Form):
    name = StringField('name', validators=[Length(min=5,max=25)])
    email= StringField('email',validators=[email_validator])
    password=StringField('password',validators=[pass_valid])



class Task_form(Form):
    task_name= StringField('task_name',validators=[task_name_checker])
    date_created=StringField('date_created',validators=[date_checker])


class Status_form(Form):
    status=StringField('status',validators=[status_check])

