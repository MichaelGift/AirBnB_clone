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
        with open(
                FileStorage.__file_path, encoding="utf-8", mode='w') as save_file:
            saves = {key: value.to_dict() for key, value, in FileStorage.__objects.items()}
            json.dump(saves, save_file)

    def reload(self):
        """
        Loads all saved basemodel instances
        """
        try:
            with open(
                    FileStorage.__file_path, mode='r', encoding='utf-8') as save_file:
                for key, value in (json.load(save_file)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass
