"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class SSQueryType(CommonInt):
    """ Query types. """
    ALL_PLUS_ANY: 'SSQueryType' = 0
    ALL_INTERSECT_ANY: 'SSQueryType' = 1
    ALL_PLUS_ANY_MUST_HAVE_ONE: 'SSQueryType' = 2
    ALL_INTERSECT_ANY_MUST_HAVE_ONE: 'SSQueryType' = 3
