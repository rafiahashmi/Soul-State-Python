# models/salah_entry.py

class SalahEntry:
    """Represents a single daily Salah log record (Fajr, Dhuhr, etc.)."""
    def __init__(self, date: str, fajr: int, dhuhr: int, asr: int, maghrib: int, isha: int, notes: str = ""):
        self.date = date
        self.fajr = fajr      # 1 or 0
        self.dhuhr = dhuhr
        self.asr = asr
        self.maghrib = maghrib
        self.isha = isha
        self.notes = notes

    def to_dict(self):
        return {
            "date": self.date,
            "fajr": self.fajr,
            "dhuhr": self.dhuhr,
            "asr": self.asr,
            "maghrib": self.maghrib,
            "isha": self.isha,
            "notes": self.notes
        }
