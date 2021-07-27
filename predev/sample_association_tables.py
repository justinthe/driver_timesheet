# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine  = create_engine('postgresql://postgres:password@localhost:5432/driver_timesheet')
Session = sessionmaker(bind=engine)
session = Session()



app=Flask("__flaskr__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/driver_timesheet'
db = SQLAlchemy(app)

admin = User(username='admin', firstname='admin', lastname='admin')
urole = UserRole(valid=True)
urole.role = Role(role='admin', description='admin')
admin.roles.append(urole)
db.session.add(urole)
db.session.commit()


# ------------------------------



driver = User(username='sopir', firstname='endang', lastname='endang')
session.add(driver)
session.commit()


dani = User(username='dani', firstname='Daniel', lastname='Boug')
sopir = Role(role='sopir', description='sopir')
urole = UserRole(valid=False)
urole.role = sopir
dani.roles.append(urole)
session.add(urole)
session.commit()



# Get Endang
# endang = session.query(User).filter(User.userid == 18).all()
endang = session.query(User).filter(User.userid == 18).one_or_none()
sopir = session.query(Role).filter(Role.roleid == 3).one_or_none()
roleSopir = UserRole(valid=False)
roleSopir.user = endang
roleSopir.role = sopir
session.add(roleSopir)


# query
sopirs = session.query(User.userid, User.username).filter(UserRole.userid == User.userid).filter(UserRole.roleid == Role.roleid).all()
session.commit()

#remove endang
sopir_endang = session.query(User).filter(User.userid == 18).one_or_none()

# it'll show [<UserRole 18, 3>]
sopir_endang.roles

# remove from UserRole
session.delete(sopir_endang.roles[0])
session.commit()

# ---------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime


engine  = create_engine('postgresql://postgres:password@localhost:5432/driver_timesheet')
Session = sessionmaker(bind=engine)
session = Session()

adminuser = session.query(User).filter(User.userid == 23).one_or_none()
time1 = Timesheet(user=adminuser, dttimeenter=datetime.now(), inout=True)

session.add(time1)
session.commit()