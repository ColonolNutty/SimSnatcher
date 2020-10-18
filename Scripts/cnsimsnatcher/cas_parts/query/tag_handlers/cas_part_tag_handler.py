"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple

from cnsimsnatcher.cas_parts.cas_part_tag_type import SSCASPartTagType
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from cnsimsnatcher.queries.tag_handler import SSTagHandler


class SSCASPartTagHandler(SSTagHandler):
    """ A filter for CAS Parts. """
    def __init__(self, tag_type: SSCASPartTagType):
        super().__init__(tag_type)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def tag_type(self) -> SSCASPartTagType:
        return super().tag_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self, cas_part: SSCASPart) -> Tuple[Any]:
        return super().get_tags(cas_part)

    # noinspection PyMissingOrEmptyDocstring
    def applies(self, cas_part: SSCASPart) -> bool:
        return super().applies(cas_part)
