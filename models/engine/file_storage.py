#!/usr/bin/env python3
"""File storage module"""
import json


class FileStorage:
    """
    Changes BaseModel instances to JSON and back.
    Enabling storage and retrieval
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Return the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets an item in the objects dictionary with the id as the key
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """
        Saves all elements in __objects to the path in __file_path
        """
        with open(FileStorage.__file_path, encoding='utf-8', mode='w') as file:
            new_d = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(new_d, file)

    def reload(self):
        """
        Loads all saved basemodel instances
        """
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass
