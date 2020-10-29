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


class SSBindingStringId(Int):
    """ LocalizedString identifiers used by SS. """
    BINDING = 3696479536
    BODY_LOCATION = 908573458
    BODY_SIDE = 1159597562
    NO_BINDINGS_FOUND = 581513238

    # Tokens: {0.String}
    BINDINGS_COUNT_STRING = 890279919

    DETACH_ALL_BINDINGS = 80137309
