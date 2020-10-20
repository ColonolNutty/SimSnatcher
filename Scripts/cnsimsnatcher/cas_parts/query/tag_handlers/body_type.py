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
from cnsimsnatcher.dtos.cas_parts.body_cas_part import SSBodyCASPart
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart


@SSCASPartQueryRegistry.register_tag_handler(filter_type=SSCASPartTagType.BODY_TYPE)
class SSBodyTypeTagHandler(SSCASPartTagHandler):
    """ Tags. """

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, cas_part: SSBodyCASPart) -> Tuple[Any]:
        return cas_part.body_type,

    # noinspection PyMissingOrEmptyDocstring
    def applies(self, cas_part: SSCASPart) -> bool:
        return isinstance(cas_part, SSBodyCASPart)
