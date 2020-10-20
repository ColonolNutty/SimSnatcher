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
from cnsimsnatcher.bindings.enums.binding_body_location import SSBindingBodyLocation
from sims.outfits.outfit_enums import BodyType


class SSBodyTypeCASPartFilter(SSCASPartTagFilter):
    """ Filter CAS Parts by Binding Body Location. """
    def __init__(self, body_type: BodyType) -> None:
        super().__init__(True, tag_type=SSCASPartTagType.BODY_TYPE)
        self._body_type = body_type

    # noinspection PyMissingOrEmptyDocstring
    def get_tags(self) -> Tuple[SSCASPartQueryTag]:
        return SSCASPartQueryTag(self.tag_type, self._body_type),

    def __str__(self) -> str:
        return '{}: {}'.format(
            self.__class__.__name__,
            self._body_type
        )
