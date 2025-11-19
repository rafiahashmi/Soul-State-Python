# models/tracker.py

import csv
import os
from abc import ABC, abstractmethod

class Tracker(ABC):
    """
    Abstract Base Class (ABC) for all specific trackers.
    Enforces the implementation of core data management methods.
    """
    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def load_entries(self):
        """Must load entries from the CSV file into self.entries."""
        pass

    @abstractmethod
    def add_entry(self, *args, **kwargs):
        """Must add or update a single entry and call self.save_all()."""
        pass

    @abstractmethod
    def save_all(self):
        """Must overwrite the entire CSV file using self.entries."""
        pass

    @abstractmethod
    def get_entries(self):
        """Must return entries as a list of dictionaries for the UI/analysis."""
        pass
