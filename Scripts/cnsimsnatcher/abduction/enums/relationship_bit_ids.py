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


class SSAbductionRelationshipBitId(Int):
    """ Relationship Bit identifiers used by SS Abduction. """
    CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT = 1826347842
    SIM_IS_CAPTIVE_OF_SIM_REL_BIT = 1469359226
    SIM_IS_CAPTOR_OF_REL_BIT = 1758575024
