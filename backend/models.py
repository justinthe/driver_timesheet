import os
from datetime import datetime 
from sqlalchemy import Column, String, Integer, create_engine, Boolean, \
        ForeignKey, DateTime, func, text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "driver_timesheet"

# database_path = "postgresql://{}:{}@{}/{}".format("postgres", "password", "localhost:5432", database_name)

db_username = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
db_connection_name = os.environ["DB_SQL_CONNECTION_NAME"]
# database_path = "postgresql://{}:{}@{}/{}".format(db_username, db_password, db_host, database_name)
database_path = "postgresql://{}:{}@/{}?host=/cloudsql/{}".format(db_username,
                                                                    db_password,
                                                                    db_name,
                                                                    db_connection_name)



db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)
    db.create_all()


class DBUtil():

    # def get_approved_timesheet(dtstart, dtend, userid):
    #     data = db.session.query(func.public.get_summary_timesheet(dtstart, dtend, userid)).all()
    #     print("Type:{}".format(len(data)))
    #     return data

   
    def call_db_function(fn_name, *args):
       data = None
       
       # get_summary_timesheet(dtstart, dtend, userid)
       if fn_name == 'get_summary_timesheet':
           data = db.session.query(func.get_summary_timesheet(args[0], args[1], args[2])).all()
       
       # get_approved_timesheet(dtstart, dtend, userid)    
       if fn_name == 'get_approved_timesheet':
           data = db.session.query(func.get_approved_timesheet(args[0], args[1], args[2])).all()

       # get_summary_rate(dtstart, dtend, userid)
       if fn_name == 'get_summary_rate':
           data = db.session.query(func.get_summary_rate(args[0], args[1], args[2])).all()
           
       print("fn_name: {}, data:{}".format(fn_name, data))
       return data

    # need to call approve data in one go to save bandwitdh. 
    # get the timesheetids, construct the sql statement from it, 
    # send statement in one go !
    def call_raw_sql(sql):
        statement = text(sql)
        data = db.session.execute(statement)
        db.session.commit()
        return data

    # def fmt_approved_timesheet(data):
    def fmt_data_from_fn(fn_name, data):
       retlist = []
    
       for outer_rows in data:
           for rows in outer_rows:
               all_words = rows.split(",")
               dct = {}

               if fn_name == 'get_approved_timesheet':
                   dct['dte'] = all_words[0][1:]
                   dct['timein'] = all_words[1][1:-1]
                   dct['timeout'] = all_words[2][1:-2]
               
               if fn_name == 'get_summary_rate' :
                   dct['dte'] = all_words[0][1:]
                   dct['hr_ot'] = all_words[1]
                   dct['holiday'] = all_words[2]
                   dct['timein'] = all_words[3][1:-1]
                   dct['timeout'] = all_words[4][1:-1]
                   dct['tot_allowance'] = all_words[5]

               retlist.append(dct)
       
       return retlist




class User(db.Model):
    __tablename__ = 'rf_user'

    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    roles = relationship("UserRole", back_populates="user")
    timesheets = relationship("Timesheet", back_populates="user")
    approvals = relationship("Approval", back_populates="user")


    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.userid,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
                }

class Role(db.Model):
    __tablename__ = "rf_role"

    roleid = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("UserRole", back_populates="role")
    
    def format(self):
        return {
            "id": self.roleid,
            "role": self.role,
            "description": self.description,
                }


class UserRole(db.Model):
    __tablename__ = "user_roles"
    userid = Column(Integer, ForeignKey('rf_user.userid'), primary_key=True) 
    roleid = Column(Integer, ForeignKey('rf_role.roleid'), primary_key=True)
    valid = Column(Boolean)

    role = relationship("Role", back_populates="users")
    user = relationship("User", back_populates="roles")

    def __init(self, user, role, valid):
        self.user = user
        self.role = role
        self.valid = valid
    
    def addUserRole(self):
        db.session.add(self)
        db.session.commit()

class Timesheet(db.Model):
    __tablename__ = "timesheet"
    timesheetid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('rf_user.userid'))
    dttimeenter = Column(DateTime, default=datetime.now)
    inout = Column(Boolean)

    user = relationship("User", back_populates="timesheets")
    timesheets = relationship("Approval", back_populates="timesheet")

    def __init__(self, user, dttimeenter,  inout):
        self.user = user
        self.dttimeenter = dttimeenter
        self.inout = inout

    def addEntry(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "timesheetid": self.timesheetid,
            "userid": self.userid,
            "dttimeenter": self.dttimeenter,
            "inout": self.inout,
                }

    
class Approval(db.Model):
    __tablename__ = "approval"
    timesheetid = Column(Integer, ForeignKey("timesheet.timesheetid"), primary_key=True)
    userid = Column(Integer, ForeignKey('rf_user.userid'))
    dttimeenter = Column(DateTime, default=datetime.now)
    approval = Column(Boolean, default=True)

    timesheet = relationship("Timesheet", back_populates="timesheets")
    user = relationship("User", back_populates="approvals")

    def __init__(self, timesheet, user,  dttimeenter, approval):
        self.timesheet = timesheet
        self.user = user
        self.dttimeenter = dttimeenter
        self.approval = approval

    def addEntry(self):
        db.session.add(self)
        db.session.commit()

    # # approve or reject
    # def approve(self, approval=True):
    #     self.approval = approval
    #     db.session.add(self)
    #     db.session.commit()

    
    def format(self):
        return {
            "timesheetid": self.timesheetid,
            "userid": self.userid,
            "dttimeenter": self.dttimeenter,
            "approval": self.approval,
                }
