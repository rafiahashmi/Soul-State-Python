# salah_tracker.py

import csv
from datetime import datetime

from models.salah_entry import SalahEntry
from models.tracker import Tracker


class SalahTracker(Tracker):
    def __init__(self, filename="data/namaz_data.csv"):
        super().__init__(filename)
        self.fieldnames = ["date", "fajr", "dhuhr", "asr", "maghrib", "isha", "notes"]
        self.entries = self.load_entries()

    def load_entries(self):
        entries = []
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    entries.append(SalahEntry(
                        row["date"], int(row["fajr"]), int(row["dhuhr"]),
                        int(row["asr"]), int(row["maghrib"]), int(row["isha"]),
                        row["notes"]
                    ))
        except FileNotFoundError:
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        return entries

    def add_entry(self, fajr: int, dhuhr: int, asr: int, maghrib: int, isha: int, notes: str = ""):
        date = datetime.now().strftime("%Y-%m-%d")

        # Update logic
        for entry in self.entries:
            if entry.date == date:
                entry.fajr, entry.dhuhr, entry.asr, entry.maghrib, entry.isha, entry.notes = \
                    fajr, dhuhr, asr, maghrib, isha, notes
                self.save_all()
                return

        # Create new entry
        new_entry = SalahEntry(date, fajr, dhuhr, asr, maghrib, isha, notes)
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
