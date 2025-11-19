# sleep_tracker.py

import csv
from datetime import date as dt

from models.sleep_entry import SleepEntry
from models.sleep import Sleep
from models.tracker import Tracker


class SleepTracker(Tracker):
    def __init__(self, filename="data/sleep.csv"):
        super().__init__(filename)
        self.fieldnames = ["date", "sleep hours", "note", "sleep_type_name"]
        self.sleep_types = [Sleep(name="Nightly Rest")]
        self.entries = self.load_entries()


    def load_entries(self):
        entries = []
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sleep_type_name = row.get("sleep_type_name", "Nightly Rest")
                    sleep_obj = next((t for t in self.sleep_types if t.name == sleep_type_name), Sleep(sleep_type_name))

                    entries.append(SleepEntry(
                        row["date"],
                        float(row["sleep hours"]),
                        row["note"],
                        sleep_type=sleep_obj
                    ))
        except FileNotFoundError:
            with open(self.filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        return entries


    def add_entry(self, hours: float, note: str = "", date: str = None, sleep_type_name: str = "Nightly Rest"):
        date = date or dt.today().isoformat()

        sleep_type = next((t for t in self.sleep_types if t.name == sleep_type_name), Sleep(name=sleep_type_name))

        # Update logic
        for entry in self.entries:
            if entry.date == date:
                entry.hours = hours
                entry.note = note
                entry.sleep_type = sleep_type
                self.save_all()
                return

        # Create new
        new_entry = SleepEntry(date, hours, note, sleep_type)
        self.entries.append(new_entry)
        self.save_all()


    def save_all(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for e in self.entries:
                writer.writerow(e.to_dict())


    def get_entries(self):
        return [
            {"date": e.date, "sleep hours": e.hours, "note": e.note, "sleep_type": e.sleep_type.name}
            for e in self.entries
        ]
