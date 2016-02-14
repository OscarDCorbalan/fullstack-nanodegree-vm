from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# EXERCICE 1: db creation, 1 shelter has many puppies

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    weight = Column(Numeric(10))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    profile = relationship("PuppyProfile", uselist = False, back_populates="puppy")


# EXERCICE 3

# 1. Each puppy is allowed one profile which can contain a url to the puppy's
# photo, a description about the puppy, and any special needs the puppy may
# have. Implement this table and the foreign key relationship in code.

class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key = True)
    picture = Column(String)
    description = Column(String(250))
    observations = Column(String(250))
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", back_populates="profile")

# 2. Puppies can be adopted by one person, or a family of people. Similarly, a
# person or family can adopt one or several puppies. See if you can create a
# many-to-many relationship between puppies and adopters

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key = True)
    name = Column(String(250))



engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
