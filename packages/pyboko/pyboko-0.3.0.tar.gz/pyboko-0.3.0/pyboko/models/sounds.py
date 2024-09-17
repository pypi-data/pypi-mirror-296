from dateutil.parser import isoparse


class SoundsData:
    def __init__(self, data):
        up = data.get("updated", None)
        if up:
            self.updated = isoparse(up)
        else:
            self.updated = up
        self.matching = data.get("matching", None)
        self.sounds = [Sound(sound) for sound in data.get("sounds", [])]


class Sound:
    def __init__(self, data):
        amt = data.get("amount", None)
        if amt:
            self.amount = float(amt / 100)
        else:
            self.amount = amt
        self.description = data.get("description", None)
        self.verified = data.get("verified", None)
        self.newsound = data.get("newsound", None)
        self.matched = data.get("matched", None)