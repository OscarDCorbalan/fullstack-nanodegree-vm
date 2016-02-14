from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from puppies import *
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# EXERCICE 2
# 2.1. Query all of the puppies and return the results in ascending alphabetical order
def getAllPuppies():
    return session.query(Puppy).order_by(asc(Puppy.name)).all()

# 2.2. Query all of the puppies that are less than 6 months old, youngest first
def getYoungPuppies():
    today = datetime.date.today()
    before = today - datetime.timedelta(days = 180)
    return session.query(Puppy).filter(Puppy.dateOfBirth.between(before, today))\
            .order_by(desc(Puppy.dateOfBirth))\
            .all()

# 2.3. Query all puppies by ascending weight
def getPuppiesByWeight():
    today = datetime.date.today()
    before = today - datetime.timedelta(days = 180)
    return session.query(Puppy).filter(Puppy.dateOfBirth.between(before, today))\
            .order_by(desc(Puppy.dateOfBirth))\
            .all()

# 2.4. Query all puppies grouped by the shelter in which they are staying
def getShelters():
    return session.query(Shelter).order_by(asc(Shelter.name)).all()

def getPuppiesInShelter(shelter):
    return session.query(Puppy).filter(Puppy.shelter == shelter)\
            .order_by(Puppy.name)\
            .all()

# EXERCISE 3 (associations)
def getPuppyProfile(puppy):
    return session.query(PuppyProfile).filter(PuppyProfile.puppy == puppy).one()


print "1. All puppies in alphabetical order:"
for puppy in getAllPuppies():
    print puppy.name

print "2. Puppies less than 6 months old in age order:"
for puppy in getYoungPuppies():
    print puppy.name, puppy.dateOfBirth

print "3. All puppies in weight order:"
for puppy in getPuppiesByWeight():
    print puppy.name, puppy.weight

print "4. Puppies grouped by shelter:"
for shelter in getShelters():
    print shelter.name
    for puppy in getPuppiesInShelter(shelter):
        print " -", puppy.name

print "5. Puppies with profiles"
for puppy in getAllPuppies():
    profile = getPuppyProfile(puppy)
    print puppy.name, profile.picture
