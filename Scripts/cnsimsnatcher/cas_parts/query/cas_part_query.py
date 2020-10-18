"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.cas_parts.cas_part_query_tag import SSCASPartQueryTag
from cnsimsnatcher.cas_parts.tag_filters.cas_part_tag_filter import SSCASPartTagFilter
from cnsimsnatcher.enums.query_type import SSQueryType
from cnsimsnatcher.queries.query import SSQuery


class SSCASPartQuery(SSQuery):
    """ A query used to locate animations. """
    def __init__(
        self,
        filters: Tuple[SSCASPartTagFilter],
        query_type: SSQueryType=SSQueryType.ALL_PLUS_ANY
    ):
        super().__init__(filters, query_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_all_tags(self) -> Tuple[SSCASPartQueryTag]:
        result: Tuple[SSCASPartQueryTag] = super().include_all_tags
        return result

    # noinspection PyMissingOrEmptyDocstring
    @property
    def include_any_tags(self) -> Tuple[SSCASPartQueryTag]:
        result: Tuple[SSCASPartQueryTag] = super().include_any_tags
        return result

    # noinspection PyMissingOrEmptyDocstring
    @property
    def exclude_tags(self) -> Tuple[SSCASPartQueryTag]:
        result: Tuple[SSCASPartQueryTag] = super().exclude_tags
        return result
