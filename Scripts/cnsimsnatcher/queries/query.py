"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Callable, List

from cnsimsnatcher.enums.query_type import SSQueryType
from cnsimsnatcher.queries.query_tag import SSQueryTag
from cnsimsnatcher.queries.tag_filter import SSTagFilter


class SSQuery:
    """ A query used to locate things. """
    def __init__(
        self,
        filters: Tuple[SSTagFilter],
        query_type: SSQueryType=SSQueryType.ALL_PLUS_ANY
    ):
        self._filters = filters
        self._query_type = query_type
        self._include_all_tags = None
        self._include_any_tags = None
        self._exclude_tags = None

    @property
    def include_all_tags(self) -> Tuple[SSQueryTag]:
        """ Must have all of these tags to match. """
        if self._include_all_tags is not None:
            return self._include_all_tags

        def _include_filter(_filter: SSTagFilter) -> bool:
            return _filter.match_all_tags and not _filter.exclude_tags

        self._include_all_tags = self._get_filter_tags(_include_filter)
        return self._include_all_tags

    @property
    def include_any_tags(self) -> Tuple[SSQueryTag]:
        """ Must have any of these tags to match. """
        if self._include_any_tags is not None:
            return self._include_any_tags

        def _include_filter(_filter: SSTagFilter) -> bool:
            return not _filter.match_all_tags and not _filter.exclude_tags

        self._include_any_tags = self._get_filter_tags(_include_filter)
        return self._include_any_tags

    @property
    def exclude_tags(self) -> Tuple[SSQueryTag]:
        """ Must NOT have any of these tags to match. """
        if self._exclude_tags is not None:
            return self._exclude_tags

        def _include_filter(_filter: SSTagFilter) -> bool:
            return _filter.match_all_tags and _filter.exclude_tags

        self._exclude_tags = self._get_filter_tags(_include_filter)
        return self._exclude_tags

    def _get_filter_tags(self, include_filter_callback: Callable[[SSTagFilter], bool]) -> Tuple[SSQueryTag]:
        tags: List[SSQueryTag] = []
        for _filter in self._filters:
            if not include_filter_callback(_filter):
                continue
            for tag in _filter.get_tags():
                tags.append(tag)
        return tuple(tags)

    @property
    def query_type(self) -> SSQueryType:
        """ The type of query. """
        return self._query_type

    def __repr__(self) -> str:
        return '{}:\n' \
               'Include All: {}\n' \
               'Include Any: {}\n' \
               'Exclude All: {}\n' \
               'Query Type: {}'\
            .format(
                self.__class__.__name__,
                pformat(self.include_all_tags),
                pformat(self.include_any_tags),
                pformat(self.exclude_tags),
                pformat(self.query_type)
            )

    def __str__(self) -> str:
        return self.__repr__()
