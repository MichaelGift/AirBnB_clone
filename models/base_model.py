#!/usr/bin/env python3

"""Define the common attributes/methods for all other classes"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """The blueprint for all other classes"""

    def __init__(self):
        """Initialize a new BaseModel."""
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

    def save(self):
        """Update the updated_at attribute to the current date and time"""
        self.updated_at = datetime.today()

    def to_dict(self):
        """Return the dictionary representation of the BaseModel instance."""
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["__class__"] = self.__class__.__name__
        return result

    def __str__(self):
        """Return the string representation of the BaseModel instance"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )
