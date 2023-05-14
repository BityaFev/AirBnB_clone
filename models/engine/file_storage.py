#!/usr/bin/env python3
"""
This module contains the FileStorage class,
which represents an abstracted storage engine.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    The FileStorage class represents an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        objdict = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, 'r') as f:
                objdict = json.load(f)
                for key, val in objdict.items():
                    cls_name = val['__class__']
                    del val['__class__']
                    self.new(eval(cls_name)(**val))
        except FileNotFoundError:
            pass
