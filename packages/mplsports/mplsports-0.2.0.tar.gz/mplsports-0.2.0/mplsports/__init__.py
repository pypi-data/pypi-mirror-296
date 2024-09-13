from .pitch.soccer import SoccerPitch
from .pitch.basketball import BasketballCourt
from .pitch.tennis import TennisCourt
from .pitch.volleyball import VolleyballCourt
from .pitch.handball import HandballCourt


class Thing:
    def __new__(cls, sport, **kwargs):
        if sport.lower() == "soccer":
            return SoccerPitch(**kwargs)
        elif sport.lower() == "basketball":
            return BasketballCourt(**kwargs)
        elif sport.lower() == "tennis":
            return TennisCourt(**kwargs)
        elif sport.lower() == "volleyball":
            return VolleyballCourt(**kwargs)
        elif sport.lower() == "handball":
            return HandballCourt(**kwargs)
        else:
            raise ValueError(f"Unsupported sport: {sport}")


Pitch = Thing
Court = Thing
Field = Thing
Ground = Thing
