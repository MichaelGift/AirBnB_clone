#!/usr/bin/env python3
"""Define unit tests for model/base_model.py module.
Unit ties classes:
    BaseModelInstantiation
    BaseModelSave
    BaseModelDictRepresentation
    BaseModelStrRepresentation
"""
import unittest
from models.base_model import BaseModel
from datetime import datetime


class BaseModelInstantiation(unittest.TestCase):
    """Test instantiation of BaseModel"""

    def test_initialization(self):
        base_model = BaseModel()
        self.assertIsInstance(base_model.id, str)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_unique_id(self):
        case1 = BaseModel()
        case2 = BaseModel()
        self.assertNotEqual(case1.id, case2.id)


class BaseModelSave(unittest.TestCase):
    """Test save of BaseModel."""

    def test_save_time(self):
        base_model = BaseModel()
        old_save = base_model.updated_at
        new_save = base_model.save()
        self.assertNotEqual(old_save, new_save)


class BaseModelDictRepresentation(unittest.TestCase):
    """Test dictionary representation of BaseModel"""

    def test_data_type(self):
        base_model = BaseModel()
        self.assertIsInstance(base_model.to_dict(), dict)

    def test_correct_keys(self):
        base_model = BaseModel()
        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())


class BaseModelStrRepresentation(unittest.TestCase):
    """Test string representation of BaseModel"""

    def test_fields_in_output(self):
        base_model = BaseModel()
        base_model.name = "Made up class name"
        self.assertIn(base_model.id, base_model.__str__())
        self.assertIn(base_model.name, base_model.__str__())
        self.assertIn(str(base_model.__dict__), base_model.__str__())
