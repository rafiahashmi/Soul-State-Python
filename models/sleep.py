# models/sleep.py

class Sleep:
    """Represents the conceptual or 'type' aspect of sleep."""
    def __init__(self, name: str = "Nightly Rest"):
        self.name = name

    def __repr__(self):
        return f"Sleep({self.name})"
