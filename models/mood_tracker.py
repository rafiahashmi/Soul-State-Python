# mood_tracker.py

import csv
from datetime import datetime

from models.mood_entry import MoodEntry
from models.mood import Mood
from models.tracker import Tracker


class MoodTracker(Tracker):
    def __init__(self, filename="data/mood_data.csv"):
        super().__init__(filename)
        self.moods = [
            Mood("Happy", 5, "#9BE7A3"),
            Mood("Calm", 4, "#6ECC8F"),
            Mood("Tired", 3, "#47B36A"),
            Mood("Sad", 2, "#2B8A45"),
            Mood("Angry", 1, "#165F2B")
        ]
        self.fieldnames = ["date", "category", "mood_score", "mood_color", "note"]
        self.entries = self.load_entries()


    def load_entries(self):
        entries = []
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    mood_obj = next((m for m in self.moods if m.name == row["category"]), None)
                    if mood_obj:
                        entries.append(MoodEntry(row["date"], mood_obj, row["note"]))
        except FileNotFoundError:
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        return entries


    def add_entry(self, mood_name: str, note: str = "", date: str = None):
        date = date or datetime.now().strftime("%Y-%m-%d")
        mood = next((m for m in self.moods if m.name == mood_name), None)

        if mood:
            # Update logic
            for entry in self.entries:
                if entry.date == date:
                    entry.mood = mood
                    entry.note = note
                    self.save_all()
                    return

            # Create new entry
            new_entry = MoodEntry(date, mood, note)
            self.entries.append(new_entry)
            self.save_all()


    def save_all(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for e in self.entries:
                writer.writerow(e.to_dict())


    def get_entries(self):
        return [e.to_dict() for e in self.entries]

    def get_available_moods(self):
        return [(m.name, m.color) for m in self.moods]
