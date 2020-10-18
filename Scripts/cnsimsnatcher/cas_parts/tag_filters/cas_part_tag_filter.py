"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from cnsimsnatcher.cas_parts.cas_part_query_tag import SSCASPartQueryTag
from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.queries.tag_filter import SSTagFilter


class SSCASPartTagFilter(SSTagFilter):
    """ A filter for use when querying CAS parts. """
    def __init__(self, match_all_tags: bool, exclude_tags: bool=False, tag_type: SSCASPartTagType=None):
        super().__init__(match_all_tags, exclude_tags=exclude_tags, tag_type=tag_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> Union[SSCASPartTagType, None]:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[SSCASPartQueryTag]:
        result: Tuple[SSCASPartQueryTag] = super().get_tags()
        return result
