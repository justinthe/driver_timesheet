import os
from datetime import datetime 
from sqlalchemy import Column, String, Integer, create_engine, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "driver_timesheet"

# database_path = "postgresql://{}:{}@{}/{}".format("postgres", "password", "localhost:5432", database_name)

db_username = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
database_path = "postgresql://{}:{}@{}/{}".format(db_username, db_password, db_host, database_name)



db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)
    db.create_all()


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
