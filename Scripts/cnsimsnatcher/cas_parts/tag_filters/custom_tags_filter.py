"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.cas_parts.cas_part_query_tag import SSCASPartQueryTag
from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.cas_parts.tag_filters.cas_part_tag_filter import SSCASPartTagFilter


class SSCustomTagsCASPartFilter(SSCASPartTagFilter):
    """ Used to specify tags for filtering. """
    def __init__(self, tags: Tuple[SSCASPartQueryTag], match_all_tags: bool=False, exclude_tags: bool=False):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=SSCASPartTagType.CUSTOM_TAG)
        self._custom_tags = tags

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[SSCASPartQueryTag]:
        return self._custom_tags

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._custom_tags
        )
