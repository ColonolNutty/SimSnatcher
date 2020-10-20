"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
from _resourceman import Key
from typing import Tuple, Union

from cnsimsnatcher.cas_parts.cas_part_tuning import SimSnatcherBodyCASPartData
from cnsimsnatcher.cas_parts.cas_part_type import SSCASPartType
from cnsimsnatcher.dtos.cas_parts.cas_part import SSCASPart
from cnsimsnatcher.dtos.cas_parts.cas_part_available_for import SSCASPartAvailableFor
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.outfits.outfit_enums import BodyType
from sims.sim_info_types import Gender, Age
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.utils.common_log_registry import CommonLog


class SSBodyCASPart(SSCASPart):
    """ Holds information related to a Body CAS part. """
    def __init__(
        self,
        part_type: SSCASPartType,
        body_type: BodyType,
        part_id: int,
        additional_part_ids: Tuple[int],
        display_name: LocalizedString,
        raw_display_name: str,
        author: str,
        available_for: SSCASPartAvailableFor,
        part_tags: Tuple[str],
        unique_identifier: Union[str, None]=None
    ):
        super().__init__(
            part_type,
            part_id,
            additional_part_ids,
            display_name,
            raw_display_name,
            author,
            available_for,
            part_tags,
            unique_identifier=unique_identifier
        )
        self._body_type = body_type

    # noinspection PyMissingOrEmptyDocstring
    @property
    def unique_identifier(self) -> str:
        if not self._unique_identifier:
            part_type_name = self.part_type.name
            part_body_type_name = self.body_type.name
            self._unique_identifier = '{}{}{}{}'.format(self.author, self.name, part_type_name, part_body_type_name)
            self._unique_identifier = ''.join((ch for ch in self._unique_identifier if ch.isalnum()))
        return self._unique_identifier

    @property
    def body_type(self) -> BodyType:
        """ The type of the Body Part. """
        return self._body_type

    @property
    def is_native(self) -> bool:
        """ Determine whether or not this Part is to be used as the native. """
        return 'NATIVE' in self.tags

    def __eq__(self, other: 'SSBodyCASPart') -> bool:
        if not isinstance(other, SSBodyCASPart):
            return False
        if self.part_id != other.part_id:
            return False
        if self.part_type != other.part_type:
            return False
        if self.body_type != other.body_type:
            return False
        return True

    def __hash__(self) -> int:
        return hash((str(self.part_id), str(self.part_type), str(self.body_type)))

    def __repr__(self) -> str:
        return '<name:{}\nunique_identifier: {}\nauthor:{}\npart_id:{}\npart_tags:{}\navailable_for:{}\npart_type:{}\npart_sub_type:{}>'\
            .format(self.name, self.unique_identifier, self.author, self.part_id, self.tags, str(self.available_for), self.part_type, self.body_type)

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def load_from_package(
        cls,
        package_body_part: 'SimSnatcherBodyCASPartData',
        log: CommonLog
    ) -> Union['SSBodyCASPart', None]:
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
        additional_part_ids: Tuple[int] = getattr(package_body_part, 'additional_part_ids', tuple())

        available_for_genders: Tuple[Gender] = tuple(getattr(package_body_part, 'available_for_genders', tuple()))
        available_for_ages: Tuple[Age] = tuple(getattr(package_body_part, 'available_for_ages', tuple()))
        available_for_species: Tuple[CommonSpecies] = tuple(getattr(package_body_part, 'available_for_species', tuple()))
        if not available_for_genders and not available_for_ages and not available_for_species:
            log.error('Failed to load CAS Part {} by {}. It is missing Available For, meaning it isn\'t available for anyone!'.format(error_display_name, author), throw=False)
            return None
        available_for = SSCASPartAvailableFor(available_for_genders, available_for_ages, available_for_species)
        part_tags: Tuple[str] = tuple(getattr(package_body_part, 'part_tags', tuple()))
        part_tags: Tuple[str] = tuple([part_tag for part_tag in part_tags if part_tag])
        part_type = getattr(package_body_part, 'part_type', SSCASPartType.NONE)
        if part_type == SSCASPartType.NONE:
            log.error('Failed to load CAS Part {} by {}. CAS Part Type is NONE, please specify a CAS Part Type!'.format(error_display_name, author), throw=False)
            return None
        part_body_type = getattr(package_body_part, 'part_body_type', BodyType.NONE)
        if part_body_type == BodyType.NONE:
            log.error('Failed to load CAS Part {} by {}. Body Type is NONE, please specify a Body Type!'.format(error_display_name, author), throw=False)
            return None
        return cls(
            part_type,
            part_body_type,
            part_id,
            additional_part_ids,
            display_name,
            raw_display_name,
            author,
            available_for,
            part_tags
        )
