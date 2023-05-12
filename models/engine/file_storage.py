#!/usr/bin/python3
"""File Storage for AirBnB project"""


import json


class FileStorage:
    """
        a class that serializes instances to a JSON file and
        deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """return all the objects"""
        return FileStorage.__objects

    def new(self, obj):
        """
            sets in __objects the obj with key
            <obj class name>.id
        """

        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
            serializes __objects to the
            JSON file (path: __file_path)
        """

        new_dict = {}
        for k, v in FileStorage.__objects.items():
            new_dict[k] = v.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(new_dict, f)

    def reload(self):
        """
            deserializes the JSON file to __objects
            (only if the JSON file (__file_path) exists
        """

        try:
            with open(FileStorage.__file_path, "r") as f:
                new_dict = json.load(f)
                for k,v in new_dict.items():
                    class_name, obj_id = k.split(".")
                    m_name = class_name.lower()
                    module = __import__(f"models.{m_name}",
                                        fromlist=[class_name])
                    class_ = getattr(module, class_name)
                    obj = class_(**v)
                    FileStorage.__objects[k] = obj
        except FileNotFoundError:
            pass