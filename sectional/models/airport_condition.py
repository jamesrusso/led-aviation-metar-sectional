from enum import Enum


class AirportCondition(Enum):
    INVALID = 'INVALID'
    INOP = 'INOP'
    VFR = 'VFR'
    MVFR = 'MVFR'
    IFR = 'IFR'
    LIFR = 'LIFR'
    NIGHT = 'NIGHT'
    NIGHT_DARK = 'NIGHT_DARK'
    SMOKE = 'SMOKE'
