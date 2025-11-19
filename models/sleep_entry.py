# models/sleep_entry.py

from models.sleep import Sleep

class SleepEntry:
    """Represents a single daily sleep log record using composition with Sleep."""
    def __init__(self, date: str, hours: float, note: str = "", sleep_type: Sleep = None):
        self.date = date
        self.hours = hours
        self.note = note
        self.sleep_type = sleep_type if sleep_type is not None else Sleep()

    def to_dict(self):
        return {
            "date": self.date,
            "sleep hours": self.hours,
            "note": self.note,
            "sleep_type_name": self.sleep_type.name
        }
