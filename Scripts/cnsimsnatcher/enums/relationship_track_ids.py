"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
from relationships.relationship_bit import RelationshipBitCollectionUid

try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass


class SSRelationshipTrackId(Int):
    """ Relationship Track identifiers used by the SS mod. """
    # Min: 0.0 Max: 5000.0
    OBEDIENCE = 3550104368


with RelationshipBitCollectionUid.make_mutable():
    setattr(RelationshipBitCollectionUid, 'SSObedience', 500)
