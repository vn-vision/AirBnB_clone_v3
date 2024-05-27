#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self._password = kwargs['password']

    @property
    def password(self):
        """Getter for password"""
        return self._password

    @password.setter
    def password(self, value):
        """Setter for password, hashing it before saving"""
        self._password = md5(value.encode()).hexdigest()

    def to_dict(self, include_password=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict()
        if not include_password:
            new_dict.pop('password', None)
        return new_dict
