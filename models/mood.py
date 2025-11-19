# models/mood.py

class Mood:
    def __init__(self, name: str, score: int, color: str):
        """Represents a mood type with a name, score, and color."""
        self.name = name
        self.score = score
        self.color = color

    def __repr__(self):
        return f"Mood({self.name}, {self.score}, {self.color})"
