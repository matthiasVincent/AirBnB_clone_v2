#!/usr/bin/python3
"""This module defines a fileStorage class to store objects in a file"""

import json


class FileStorage:
    """serializes instances to a json file
    and deserializes a json file into inst
    ances.
    __file_path: private class attributes
    for file path in .json
    __objects: private class attributes to
    store dictionary of objects"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary of objs of cls
        if None, returns __objects"""
        from models.base_model import BaseModel
        from models.state import State
        from models.user import User
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        dict_of_classes = {
                "BaseModel": BaseModel, "State": State,
                "User": User, "City": City,
                "Place": Place, "Review": Review,
                "Amenity": Amenity
                }
        if cls is not None:
            objs = {
                    k: str(v) for k, v in self.__objects.items()
                    if dict_of_classes[k.split(".")[0]] == cls}
            return objs
        return self.__objects

    def new(self, obj):
        """sets in __objects, the obj with
        key <obj class name>.id"""
        class_name = obj.__class__.__name__
        key = "{}.{}".format(class_name, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to a json file"""
        with open(self.__file_path, 'w') as f:
            obj_dicts = {
                    key: values.to_dict()
                    for key, values in self.__objects.items()
                    }
            json.dump(obj_dicts, f)

    def delete(self, obj=None):
        """delete obj from __objects if present
        otherwise do nothing"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[key]

    def reload(self):
        """deserializes the json file to __objects
        only if __file_path exists, otherwise
        do nothing with no exception raised"""

        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        dict_of_class = {
                "BaseModel": BaseModel, "User": User,
                "State": State, "City": City,
                "Place": Place, "Review": Review,
                "Amenity": Amenity
                }
        try:
            with open(self.__file_path, 'r') as f:
                read_values = f.read()
                loaded_dicts = json.loads(read_values)
                for indv_dict in loaded_dicts.values():
                    class_name = indv_dict["__class__"]
                    del indv_dict["__class__"]
                    obj = dict_of_class[class_name](**indv_dict)
                    self.new(obj)
        except FileNotFoundError:
            return
