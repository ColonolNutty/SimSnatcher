"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple
from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.queries.query_tag import SSQueryTag


class SSCASPartQueryTag(SSQueryTag):
    """ A query tag. """
    def __init__(self, tag_type: SSCASPartTagType, value: Any):
        super().__init__(tag_type, value)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> SSCASPartTagType:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    @property
    def key(self) -> Tuple[SSCASPartTagType, Any]:
        return super().key
