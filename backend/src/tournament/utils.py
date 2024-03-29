from enum import Enum


class PlayerStatus(Enum):
    WAITING: str = "WAITING"
    ACCEPTED: str = "ACCEPTED"
    DECLINED: str = "DECLINED"
    BANNED: str = "BANNED"


class TournamentStatus(Enum):
    WAITING: str = "WAITING"
    RUNNING: str = "RUNNING"
    ENDED: str = "ENDED"