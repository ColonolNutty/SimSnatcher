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


class SSBuffId(Int):
    """ Buff identifiers used by SS. """
    ALLOWED_NOTHING_INVISIBLE = 14606159824511998137
    ALLOWED_BARTENDING_INVISIBLE = 13221969958789686906
    ALLOWED_BATHING_INVISIBLE = 308864153663263335
    PREVENT_LEAVE_INVISIBLE = 17783615372645687397
