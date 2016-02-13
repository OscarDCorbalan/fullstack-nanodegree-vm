from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# 1. Query all of the puppies and return the results in ascending alphabetical order
print "1. All puppies in alphabetical order"
puppies = session.query(Puppy.name)\
            .order_by(asc(Puppy.name))\
            .all()
for puppy in puppies:
    print puppy.name


# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
print "2. Puppies less than 6 months old in age order"
today = datetime.date.today()
before = today - datetime.timedelta(days = 180)
puppies = session.query(Puppy)\
            .filter(Puppy.dateOfBirth.between(before, today))\
            .order_by(desc(Puppy.dateOfBirth))\
            .all()
for puppy in puppies:
    print puppy.name, puppy.dateOfBirth


# 3. Query all puppies by ascending weight
print "3. All puppies in weight order"
puppies = session.query(Puppy)\
            .order_by(asc(Puppy.weight))\
            .all()
for puppy in puppies:
    print puppy.name, puppy.weight


# 4. Query all puppies grouped by the shelter in which they are staying
print "4. Puppies grouped by shelter"
shelters = session.query(Shelter).order_by(asc(Shelter.name)).all()
for shelter in shelters:
    print shelter.name
    puppies = session.query(Puppy)\
                .filter(Puppy.shelter == shelter)\
                .order_by(Puppy.name)\
                .all()
    for puppy in puppies:
        print " -", puppy.name
