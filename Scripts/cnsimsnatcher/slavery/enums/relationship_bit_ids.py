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


class SSSlaveryRelationshipBitId(Int):
    """ Relationship Bit identifiers used by SS Slavery. """
    MASTER_SIM_TO_SLAVE_SIM_REL_BIT = 1480977330
    SIM_IS_SLAVE_OF_SIM_REL_BIT = 42834044
    SIM_IS_MASTER_OF_SIM_REL_BIT = 1350192551
