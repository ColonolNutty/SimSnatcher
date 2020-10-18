"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import collections
import time
from pprint import pformat
from typing import Union, List, Dict, Any, Tuple, Set, Callable

from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.cas_parts.query.cas_part_query import SSCASPartQuery
from cnsimsnatcher.cas_parts.query.tag_handlers.cas_part_tag_handler import SSCASPartTagHandler
from cnsimsnatcher.cas_parts.tag_filters.cas_part_tag_filter import SSCASPartTagFilter
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService
from cnsimsnatcher.enums.query_type import SSQueryType
from cnsimsnatcher.modinfo import ModInfo


class SSCASPartQueryRegistry(CommonService, HasLog):
    """ Registry handling CAS part queries. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_cas_part_query_registry'

    @property
    def _tag_handlers(self) -> List[SSCASPartTagHandler]:
        return self.__tag_handlers

    @property
    def cas_part_library(self) -> Dict[Tuple[SSCASPartTagType, Any], Set[SSCASPart]]:
        """ A library of CAS parts organized by filter keys. """
        return self._cas_part_library

    @cas_part_library.setter
    def cas_part_library(self, value: Dict[Tuple[SSCASPartTagType, Any], Set[SSCASPart]]):
        self._cas_part_library = value

    def __init__(self) -> None:
        from cnsimsnatcher.cas_parts.cas_part_registry import SSCASPartRegistry
        super().__init__()
        self.cas_part_library = collections.defaultdict(set)
        self.__tag_handlers: List[SSCASPartTagHandler] = list()
        self._all: List[SSCASPart] = list()
        self._available: List[SSCASPart] = list()
        self._available_identifiers: Dict[str, SSCASPart] = list()
        self._registry = SSCASPartRegistry()

    def add_tag_handler(self, tag_handler_init: Callable[[SSCASPartTagType], SSCASPartTagHandler], tag: SSCASPartTagType):
        """ Add a query filter. """
        self.__tag_handlers.append(tag_handler_init(tag))

    def create_query(self, cas_part_filters: Tuple[SSCASPartTagFilter], query_type: SSQueryType=SSQueryType.ALL_PLUS_ANY) -> SSCASPartQuery:
        """ Create a query for CAS Parts. """
        return SSCASPartQuery(cas_part_filters, query_type=query_type)

    def has_cas_parts(self, queries: Tuple[SSCASPartQuery]) -> bool:
        """ Determine if CAS Parts are available for tags. """
        self.log.format_with_message('Checking if has CAS Parts', queries=queries)
        return len(tuple(self.get_cas_parts(queries))) > 0

    def get_cas_parts(self, queries: Tuple[SSCASPartQuery]) -> Tuple[SSCASPart]:
        """ Determine if CAS Parts are available for tags. """
        self.log.format_with_message('Getting CAS Parts', queries=queries)
        cas_parts = set()
        for query in queries:
            found = self._query_cas_parts(query)
            if found:
                cas_parts = cas_parts | found
        return tuple(cas_parts)

    def _query_cas_parts(self, query: SSCASPartQuery) -> Set[SSCASPart]:
        self.log.format_with_message('Querying for CAS Parts using query: {}'.format(query))
        all_tags = query.include_all_tags
        any_tags = query.include_any_tags
        exclude_tags = query.exclude_tags
        found_cas_parts = None
        for include_all_tag in all_tags:
            if include_all_tag is None:
                continue
            self.log.debug('Looking for tag {}'.format(include_all_tag))
            if include_all_tag.key not in self.cas_part_library:
                # One of the All keys is not within the CAS Part library! This means no CAS Parts match ALL tags.
                return set()
            new_found_cas_parts = self.cas_part_library[include_all_tag.key]
            if found_cas_parts is not None:
                self.log.debug('Before intersect for all_tags {}'.format(len(found_cas_parts)))
                new_found_cas_parts = found_cas_parts & new_found_cas_parts
                self.log.debug('After intersect for all_tags {}'.format(len(new_found_cas_parts)))
            else:
                self.log.debug('Found with all_tags {}'.format(len(new_found_cas_parts)))
            found_cas_parts = new_found_cas_parts

        if found_cas_parts is None and all_tags:
            self.log.debug('No CAS Parts found for all_tags {}'.format(all_tags))
            return set()

        self.log.debug('After all_tags {}'.format(len(found_cas_parts)))
        # self.log.debug('Found CAS Parts for all_tags {}'.format(',\n'.join(['{}:{}:({})'.format(str(found_cas_part.raw_display_name), found_cas_part.author, found_cas_part.locations) for found_cas_part in found_cas_parts])))

        found_cas_parts_via_any_tags = set()
        for include_any_tag in any_tags:
            if include_any_tag is None:
                continue
            if include_any_tag.key not in self.cas_part_library:
                continue
            found_cas_parts_via_any_tags = found_cas_parts_via_any_tags | self.cas_part_library[include_any_tag.key]

        # self.log.debug('Found CAS Parts via any tags {}'.format(',\n'.join(['{}:{}'.format(str(found_cas_part_via_any_tags.raw_display_name), found_cas_part_via_any_tags.author) for found_cas_part_via_any_tags in found_cas_parts_via_any_tags])))

        if found_cas_parts is None:
            self.log.debug('No CAS Parts found for all_tags.')
            if not all_tags:
                self.log.debug('Returning any tags.')
                return found_cas_parts_via_any_tags
        else:
            query_type = query.query_type
            if query_type == SSQueryType.ALL_PLUS_ANY:
                found_cas_parts = found_cas_parts | found_cas_parts_via_any_tags
            elif query_type == SSQueryType.ALL_INTERSECT_ANY:
                found_cas_parts = found_cas_parts & found_cas_parts_via_any_tags

            if query_type == SSQueryType.ALL_PLUS_ANY_MUST_HAVE_ONE:
                if not found_cas_parts_via_any_tags:
                    return set()
                found_cas_parts = found_cas_parts | found_cas_parts_via_any_tags
            elif query_type == SSQueryType.ALL_INTERSECT_ANY_MUST_HAVE_ONE:
                if not found_cas_parts_via_any_tags:
                    return set()
                found_cas_parts = found_cas_parts & found_cas_parts_via_any_tags

        if found_cas_parts is None:
            self.log.debug('No found CAS Parts after combining any tags. All Tags: {} Any Tags: {}'.format(all_tags, any_tags))
            return set()

        self.log.debug('After any tags {}'.format(len(found_cas_parts)))

        excluded = set()
        for exclude_tag in exclude_tags:
            if exclude_tag is None:
                continue
            if exclude_tag.key not in self.cas_part_library:
                continue
            excluded = excluded | self.cas_part_library[exclude_tag.key]

        self.log.debug('Excluding CAS Parts {}'.format(len(excluded)))

        if excluded:
            found_cas_parts = found_cas_parts - excluded

        self.log.debug('After exclude CAS Parts {}'.format(len(found_cas_parts)))

        self.log.debug('Returning CAS Parts [{}]'.format(',\n'.join(['{}:{}'.format(str(found_cas_part.raw_display_name), found_cas_part.author) for found_cas_part in found_cas_parts])))
        return found_cas_parts

    def get_all(self) -> Tuple[SSCASPart]:
        """ Get all CAS Parts. """
        return tuple(self._all)

    def get_available(self) -> Tuple[SSCASPart]:
        """ Get available CAS Parts. """
        return tuple(self._available)

    def get_available_from_identifier(self, identifier: str) -> Union[SSCASPart, None]:
        """ Locate an available CAS Part by it's name. """
        if identifier and identifier in self._available_identifiers:
            return self._available_identifiers[identifier]

    def _organize(self, cas_parts: Tuple[SSCASPart]):
        self.log.debug('Collecting CAS Part Query Data...')
        self.cas_part_library.clear()
        for cas_part in cas_parts:
            self.log.debug('Handling tags for CAS part {}'.format(cas_part.raw_display_name))
            cas_part_tag_keys = list()
            for tag_handler in self._tag_handlers:
                if not tag_handler.applies(cas_part):
                    continue
                tag_type = tag_handler.tag_type
                for cas_part_tag in tag_handler.get_tags(cas_part):
                    tag_key = (tag_type, cas_part_tag)
                    cas_part_tag_keys.append(tag_key)
                    if tag_key not in self.cas_part_library:
                        self.cas_part_library[tag_key] = set()
                    if cas_part in self.cas_part_library[tag_key]:
                        continue
                    self.cas_part_library[tag_key].add(cas_part)
            self.log.debug('Applied tags to CAS Part {}: {}'.format(cas_part.raw_display_name, cas_part_tag_keys))

        self.log.debug('Completed collecting CAS Part Query Data. {}'.format(pformat(self.cas_part_library)))

    def recollect(self, include_available: bool=True):
        """ Collect CAS Parts. """
        recollect_all = not bool(self._all)
        recollect_available = include_available or not bool(self._available)
        ts = time.perf_counter()
        (all_list, available_list, available_identifiers) = self._registry.collect(
            collect_all=recollect_all,
            collect_available=recollect_available
        )
        self.log.format_with_message(
            'Loaded CAS Parts',
            all_list=all_list,
            available_list=available_list,
            available_identifiers=available_identifiers
        )
        self.log.debug('Took {}s to collect and organize CAS Parts.'.format('%.3f' % (time.perf_counter() - ts)))
        if all_list:
            self._all = all_list
        if available_list:
            self._available = available_list
            self._available_identifiers = available_identifiers
        ts = time.perf_counter()
        self._organize(self._available)
        self.log.debug('Took {}s to recollect CAS Parts'.format('%.3f' % (time.perf_counter() - ts)))
        self.log.debug('Loaded {} CAS Parts.'.format(len(self.get_available())))

    @classmethod
    def register_tag_handler(cls, filter_type: SSCASPartTagType) -> Callable[[Any], Any]:
        """ Register a tag handler. """
        def _method_wrapper(tag_handler_callback: Callable[[SSCASPartTagType], SSCASPartTagHandler]):
            cls().add_tag_handler(tag_handler_callback, filter_type)
            return tag_handler_callback
        return _method_wrapper

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _load_cas_parts_on_zone_load(event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            # If the game is already loaded, we've already loaded the data once.
            return False
        SSCASPartQueryRegistry().recollect(include_available=False)
        return True
