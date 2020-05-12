"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class SSRelationshipBitId(Int):
    """ Relationship Bit identifiers used by the SS mod. """
    NO_OBEDIENCE = 832837799
    LOW_OBEDIENCE = 3188358898
    MEDIUM_OBEDIENCE = 4197058299
    HIGH_OBEDIENCE = 2721362982
    FULL_OBEDIENCE = 1486572297
