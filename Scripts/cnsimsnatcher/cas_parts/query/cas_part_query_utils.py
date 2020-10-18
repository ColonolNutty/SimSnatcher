"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from typing import Tuple, Set, Iterator
from cnsimsnatcher.cas_parts.cas_part_type import SSCASPartType
from cnsimsnatcher.cas_parts.query.cas_part_query import SSCASPartQuery
from cnsimsnatcher.cas_parts.tag_filters.cas_part_tag_filter import SSCASPartTagFilter
from cnsimsnatcher.cas_parts.tag_filters.cas_part_type_filter import SSCASPartTypeCASPartFilter
from cnsimsnatcher.cas_parts.tag_filters.sim_filter import SSSimCASPartFilter
from cnsimsnatcher.cas_parts.tag_filters.tags_filter import SSTagsCASPartFilter
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.enums.query_type import SSQueryType

from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class SSCASPartQueryUtils(HasLog):
    """ Query for CAS parts using various filter configurations. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_cas_part_utils'

    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.cas_parts.cas_part_query_registry import SSCASPartQueryRegistry
        self.query_registry = SSCASPartQueryRegistry()

    def get_available(self) -> Tuple[SSCASPart]:
        """ Get available CAS Parts. """
        return self.query_registry.get_available()

    def has_cas_parts_for_sim(
        self,
        sim_info: SimInfo,
        cas_part_type: SSCASPartType,
        ignore_cas_parts: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[SSCASPartTagFilter]=()
    ) -> bool:
        """has_cas_parts_for_sim(\
            sim_info,\
            cas_part_type,\
            ignore_cas_parts=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Determine if CAS Parts exist for the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cas_part_type: The CAS Part type.
        :type cas_part_type: SSCASPartType
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_cas_parts: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_cas_parts: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[SSCASPartTagFilter], optional.
        :return: True, if CAS Parts exist for the criteria. False, if not.
        :rtype: bool
        """
        self.log.format_with_message(
            'Checking if CAS Parts exist for Sim.',
            sim_name=CommonSimNameUtils.get_full_name(sim_info),
            cas_part_type=cas_part_type,
            additional_filters=additional_filters,
            ignore_cas_parts=ignore_cas_parts,
            additional_tags=additional_tags
        )
        filters: Tuple[SSCASPartTagFilter] = (
            SSSimCASPartFilter(sim_info),
            SSCASPartTypeCASPartFilter(cas_part_type),
            SSTagsCASPartFilter(additional_tags),
            *additional_filters
        )
        # Include Object Tag, Include Category Tag

        queries: Tuple[SSCASPartQuery] = (self.query_registry.create_query(filters, query_type=SSQueryType.ALL_PLUS_ANY),)
        return self.query_registry.has_cas_parts(queries)

    def get_cas_parts_for_sim(
        self,
        sim_info: SimInfo,
        cas_part_type: SSCASPartType,
        ignore_cas_parts: Tuple[str]=(),
        additional_tags: Tuple[str]=(),
        additional_filters: Iterator[SSCASPartTagFilter]=()
    ) -> Tuple[SSCASPart]:
        """get_cas_parts_for_sim(\
            sim_info,\
            cas_part_type,\
            ignore_cas_parts=(),\
            additional_tags=(),\
            additional_filters=()\
        )

        Retrieve CAS Parts using the criteria.

        :param sim_info: An instance of a Sim
        :type sim_info: SimInfo
        :param cas_part_type: The CAS Part type.
        :type cas_part_type: SSCASPartType
        :param additional_tags: Additional tags to add to the query. Default is an empty collection.
        :type additional_tags: Tuple[Any], optional
        :param ignore_cas_parts: A collection of identifiers to ignore. Default is an empty collection.
        :type ignore_cas_parts: Tuple[str], optional
        :param additional_filters: Additional filters. Default is an empty collection.
        :type additional_filters: Iterator[SSCASPartTagFilter], optional.
        :return: A collection of CAS Parts matching the criteria.
        :rtype: Set[SSCASPart]
        """
        self.log.format_with_message(
            'Get CAS Parts for Sim.',
            sim_name=CommonSimNameUtils.get_full_name(sim_info),
            cas_part_type=cas_part_type,
            additional_filters=tuple(additional_filters),
            ignore_cas_parts=ignore_cas_parts,
            additional_tags=additional_tags
        )
        filters: Tuple[SSCASPartTagFilter] = (
            SSSimCASPartFilter(sim_info),
            SSCASPartTypeCASPartFilter(cas_part_type),
            SSTagsCASPartFilter(additional_tags),
            *tuple(additional_filters)
        )
        # Include Object Tag, Include Category Tag

        queries: Tuple[SSCASPartQuery] = (self.query_registry.create_query(filters, query_type=SSQueryType.ALL_PLUS_ANY),)
        return tuple(self.query_registry.get_cas_parts(queries))
