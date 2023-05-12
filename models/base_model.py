#!/usr/bin/python3
"""
    BaseModel
    Author: Feven Yohannes
"""


from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
        a class BaseModel that defines all common
        attributes/methods for other classes
    """

    def __init__(self, *args, **kwargs):
        """Initialize the class"""

        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k in ['created_at', 'updated_at']:
                    s_format = "%Y-%m-%dT%H:%M:%S.%f"
                    self.__dict__[k] = datetime.strptime(v, s_format)
                if k != '__class__':
                    setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """
            String represenation of the class
        """

        return '[{}] ({}) <{}>'.format(
                                       type(self).__name__,
                                       self.id,
                                       self.__dict__)

    def save(self):
        """
            updates the public instance attribute updated_at
            with the current datetime
        """

        self.updated_at = datetime.now()

    def to_dict(self):
        """
            returns a dictionary containing all keys/values of
            __dict__ of the instance:
        """

        new_dict = self.__dict__.copy()
        new_dict['__class__'] = type(self).__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()

        return new_dict
