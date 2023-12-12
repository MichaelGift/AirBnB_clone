#!/usr/bin/python3
"""This Defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city.
    Attributes:
        name (str): The name of the city.
        state_id (str): The state id.
    """

    state_id = ""
    name = ""
