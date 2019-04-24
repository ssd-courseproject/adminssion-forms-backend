from enum import Enum


class EnumExtended(Enum):
    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def values(cls):
        return list(map(lambda c: c.values, cls))

    @classmethod
    def list(cls):
        return {i.name: i.value for i in cls}


class UsersRole(EnumExtended):
    CANDIDATE = 1
    STAFF = 2
    MANAGER = 4


class Gender(EnumExtended):
    FEMALE = False
    MALE = True


class CandidateStatus(EnumExtended):
    PENDING = 1
    FAILED = 4
    PASSED = 5
