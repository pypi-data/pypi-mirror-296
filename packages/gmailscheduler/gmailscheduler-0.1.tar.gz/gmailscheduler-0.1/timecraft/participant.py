class Participant:
    def __init__(self, name, timezone='UTC', availability='weekdays 9am-5pm'):
        self.name = name
        self.timezone = timezone
        self.availability = availability

    def __repr__(self):
        return f"Participant(name={self.name}, timezone={self.timezone}, availability={self.availability})"
