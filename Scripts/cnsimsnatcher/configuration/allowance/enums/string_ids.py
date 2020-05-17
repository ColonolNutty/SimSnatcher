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


class SSAllowanceStringId(Int):
    """ LocalizedString identifiers used by SS Abduction. """
    # Main
    CHANGE_ALLOWANCE_NAME = 376766106
    CHANGE_ALLOWANCE_DESCRIPTION = 789434727

    # Allowances
    ALLOWED_BARTENDING = 2521032657
    ALLOWED_BATHING = 320825170
    ALLOWED_CLEANING = 2567481909
    ALLOWED_COMPUTER = 3842171293
    ALLOWED_COOKING = 3052191434
    ALLOWED_DANCING = 2712695575
    ALLOWED_EATING = 1646591416
    ALLOWED_GRAB_SNACK = 1888445371
    ALLOWED_GUEST = 3448491036
    ALLOWED_HIRED_WORKER = 2626152148
    ALLOWED_HOST = 3238770314
    ALLOWED_PHONE = 1206986714
    ALLOWED_PLAYING_INSTRUMENTS = 924233006
    ALLOWED_READ_BOOK = 2859200512
    ALLOWED_SLEEPING = 2468810951
    ALLOWED_SOCIAL = 1236713387
    ALLOWED_WORK = 2954181160
    ALLOWED_SINGING = 2223956951
    ALLOWED_STEREO = 2472852968
    ALLOWED_TV_WATCHING = 1085944699
    ALLOWED_TIP = 223701001
    ALLOWED_VIEW = 499113642
    ALLOWED_WORKOUT = 2119759267
    ALLOWED_PLAYING = 2381468829
