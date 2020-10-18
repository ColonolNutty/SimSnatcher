"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any

from cnsimsnatcher.cas_parts.cas_part_query_registry import SSCASPartQueryRegistry
from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.cas_parts.query.tag_handlers.cas_part_tag_handler import SSCASPartTagHandler
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart


@SSCASPartQueryRegistry.register_tag_handler(filter_type=SSCASPartTagType.CUSTOM_TAG)
class SSCustomTagsCASPartTagHandler(SSCASPartTagHandler):
    """ Tags. """

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, cas_part: SSCASPart) -> Tuple[Any]:
        return tuple(cas_part.tags)

    # noinspection PyMissingOrEmptyDocstring
    def applies(self, cas_part: SSCASPart) -> bool:
        return len(cas_part.tags) > 0
