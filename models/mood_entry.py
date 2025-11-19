# models/mood_entry.py

from models.mood import Mood

class MoodEntry:
    """Represents a single daily mood entry using composition with Mood."""
    def __init__(self, date: str, mood: Mood, note: str):
        self.date = date
        self.mood = mood
        self.note = note

    def to_dict(self):
        return {
            "date": self.date,
            "category": self.mood.name,
            "mood_score": self.mood.score,
            "mood_color": self.mood.color,
            "note": self.note
        }
