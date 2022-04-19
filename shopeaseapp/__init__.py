'''we actually do all our imporing in the innit'''
from flask import Flask
from flask_wtf.csrf import CSRFProtect#ACTIVATING CSRF PROTECT
from flask_sqlalchemy import SQLAlchemy#importingsql alchemy
#instantiate an object of class
app=Flask(__name__, instance_relative_config=True)
#instantatie an object of the importrd CSRF protect
csrf=CSRFProtect(app)
#local import starts here..i.e this are things impoerted between pages not from flask

#load the config
from shopeaseapp import config
app.config.from_object(config.ProductionConfig)#way of identifiting the  class config file..also production config is the name of the class in the config outside  instance
app.config.from_pyfile('config.py',silent=False)#

db=SQLAlchemy(app)#instantating sqlalchemy as db
#load your routes here i.e importing the already defined routes in route.py
from shopeaseapp.myroutes import adminroutes ,userroutes
from shopeaseapp import forms
from shopeaseapp import mymodel