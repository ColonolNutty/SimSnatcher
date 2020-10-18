"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
from _resourceman import Key
from typing import Tuple, Union, TYPE_CHECKING

from cnsimsnatcher.enums.binding_body_location import SSBindingBodyLocation
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info_types import Gender, Age
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.common_log_registry import CommonLog
from cnsimsnatcher.cas_parts.cas_part_type import SSCASPartType
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from cnsimsnatcher.dtos.cas_parts.cas_part_available_for import DDCASPartAvailableFor

if TYPE_CHECKING:
    from cnsimsnatcher.cas_parts.cas_part_tuning import SimSnatcherBindingCASPartData


class SSBindingCASPart(SSCASPart):
    """ Holds information related to a Binding CAS part. """
    def __init__(
        self,
        icon_id: Union[int, Key],
        binding_body_location: SSBindingBodyLocation,
        part_id: int,
        additional_part_ids: Tuple[int],
        display_name: LocalizedString,
        raw_display_name: str,
        author: str,
        available_for: DDCASPartAvailableFor,
        part_tags: Tuple[str],
        unique_identifier: Union[str, None]=None
    ):
        super().__init__(
            SSCASPartType.BINDING,
            part_id,
            additional_part_ids,
            display_name,
            raw_display_name,
            author,
            available_for,
            part_tags,
            unique_identifier=unique_identifier
        )
        self._binding_body_location = binding_body_location
        self._icon_id = icon_id

    # noinspection PyMissingOrEmptyDocstring
    @property
    def unique_identifier(self) -> str:
        if not self._unique_identifier:
            part_type_name = self.part_type.name
            part_sub_type_name = self.body_location.name
            self._unique_identifier = '{}{}{}{}'.format(self.author, self.name, part_type_name, part_sub_type_name)
            self._unique_identifier = ''.join((ch for ch in self._unique_identifier if ch.isalnum()))
        return self._unique_identifier

    @property
    def icon_id(self) -> Key:
        """ Decimal identifier of the Icon of the Body part. """
        if isinstance(self._icon_id, Key):
            return self._icon_id
        if self._icon_id <= 0:
            return None
        return CommonIconUtils._load_icon(self._icon_id)

    @property
    def body_location(self) -> SSBindingBodyLocation:
        """ The location of the CAS Part. """
        return self._binding_body_location

    def __eq__(self, other: 'SSBindingCASPart') -> bool:
        if not isinstance(other, SSBindingCASPart):
            return False
        if self.part_id != other.part_id:
            return False
        if self.part_type != other.part_type:
            return False
        if self.body_location != other.body_location:
            return False
        return True

    def __hash__(self) -> int:
        return hash((str(self.part_id), str(self.part_type), str(self.body_location)))

    def __repr__(self) -> str:
        return '<name:{}\nunique_identifier: {}\nauthor:{}\npart_id:{}\npart_tags:{}\navailable_for:{}\npart_type:{}\npart_sub_type:{}>'\
            .format(self.name, self.unique_identifier, self.author, self.part_id, self.tags, str(self.available_for), self.part_type, self.body_location)

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def load_from_package(
        cls,
        package_body_part: 'SimSnatcherBindingCASPartData',
        log: CommonLog
    ) -> Union['SSBindingCASPart', None]:
        display_name = getattr(package_body_part, 'part_display_name', None)
        raw_display_name = getattr(package_body_part, 'part_raw_display_name', None)
        error_display_name = raw_display_name or display_name
        author = getattr(package_body_part, 'part_author', None)
        if not author:
            log.error('Failed to load CAS Part {}. Author is missing!'.format(error_display_name), throw=False)
            return None
        part_id = getattr(package_body_part, 'part_id', 0)
        if part_id == 0:
            log.error('Failed to load CAS Part {} by {}. Missing CAS Part Id.'.format(error_display_name, author), throw=False)
            return None
        display_icon = getattr(package_body_part, 'part_display_icon', None)
        additional_part_ids: Tuple[int] = getattr(package_body_part, 'additional_part_ids', tuple())

        available_for_genders: Tuple[Gender] = tuple(getattr(package_body_part, 'available_for_genders', tuple()))
        available_for_ages: Tuple[Age] = tuple(getattr(package_body_part, 'available_for_ages', tuple()))
        available_for_species: Tuple[CommonSpecies] = tuple(getattr(package_body_part, 'available_for_species', tuple()))
        if not available_for_genders and not available_for_ages and not available_for_species:
            log.error('Failed to load CAS Part {} by {}. It is missing Available For, meaning it isn\'t available for anyone!'.format(error_display_name, author), throw=False)
            return None
        available_for = DDCASPartAvailableFor(available_for_genders, available_for_ages, available_for_species)
        part_tags: Tuple[str] = tuple(getattr(package_body_part, 'part_tags', tuple()))
        part_tags: Tuple[str] = tuple([part_tag for part_tag in part_tags if part_tag])
        binding_body_location = getattr(package_body_part, 'body_location', SSBindingBodyLocation.NONE)
        if binding_body_location == SSBindingBodyLocation.NONE:
            log.error('Failed to load CAS Part {} by {}. It is missing the body location!'.format(error_display_name, author), throw=False)
            return None
        return cls(
            display_icon,
            binding_body_location,
            part_id,
            additional_part_ids,
            display_name,
            raw_display_name,
            author,
            available_for,
            part_tags
        )
