#!usr/bin/env python3
"""Load all saved data when package is imported"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
