from enum import Enum


class PermJWT(Enum):
    ENCTYPT = 0b0001
    DECRYPT = 0b0010
    SIGNATURE = 0b0100
    VERIFY = 0b1000
