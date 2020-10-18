"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.cas_parts.cas_part_query_tag import SSCASPartQueryTag
from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.cas_parts.cas_part_type import SSCASPartType
from cnsimsnatcher.cas_parts.tag_filters.cas_part_tag_filter import SSCASPartTagFilter


class SSCASPartTypeCASPartFilter(SSCASPartTagFilter):
    """ Filter CAS Parts by CAS Part Type. """
    def __init__(self, part_type: SSCASPartType) -> None:
        super().__init__(True, tag_type=SSCASPartTagType.CAS_PART_TYPE)
        self._part_type = part_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[SSCASPartQueryTag]:
        return SSCASPartQueryTag(self.tag_type, self._part_type),

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._part_type
        )
