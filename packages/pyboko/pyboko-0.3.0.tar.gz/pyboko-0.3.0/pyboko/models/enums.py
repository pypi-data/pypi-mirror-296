from enum import Enum


class AttendeeRank(Enum):
    """
    An enum containing the possible attendee ranks
    """

    ACTIVE      = ("1", "Active")
    INACTIVE    = ("2", "Inactive")
    GUEST       = ("3", "Guest")
    CHARITY_REP = ("4", "Charity Rep")
    OTHER       = ("5", "Other")

    def __init__(self, rank_num, rank_name):
        self.rank_num = rank_num
        self.rank_name = rank_name
    
    @classmethod
    def from_rank_num(cls, rank_num):
        """
        Gets the rank from the rank number
        """
        return next((rank for rank in cls if rank.rank_num == rank_num), None)


class RunnerRank(Enum):
    """
    An enum containing the possible runner ranks
    """
    HOST        = (0, "Host")
    COMMENTARY  = (1, "Commentary")
    PARTICIPANT = (2, "Participant")

    def __init__(self, rank_num, rank_name):
        self.rank_num = rank_num
        self.rank_name = rank_name
    
    @classmethod
    def from_rank_num(cls, rank_num):
        """
        Gets the rank from the rank number
        """
        return next((rank for rank in cls if rank.rank_num == rank_num), None)