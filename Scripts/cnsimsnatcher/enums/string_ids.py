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


class SSStringId(Int):
    """ LocalizedString identifiers used by SS. """
    SIM_SNATCHER = 1121220694
    SIM_SNATCHER_SETTINGS_NAME = 4184531491
    SIM_SNATCHER_SETTINGS_DESCRIPTION = 2980311872
    CHEAT_SETTINGS_NAME = 1575501605
    CHEAT_SETTINGS_DESCRIPTION = 2391887144

    SIM_RELEASED = 3527089551
    # Tokens: {0.SimFirstName} {0.SimLastName}
    SIM_HAS_BEEN_RELEASED_PLEASE_WAIT = 4083959082

    NOT_ALLOWED = 3305495264
    YOUR_MASTER_HAS_FORBIDDEN_THAT_INTERACTION = 1785112478
    YOUR_CAPTOR_HAS_FORBIDDEN_THAT_INTERACTION = 2936117011
