"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from cnsimsnatcher.modinfo import ModInfo
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_species import CommonSpecies
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from cnsimsnatcher.cas_parts.cas_part_type import SSCASPartType
from cnsimsnatcher.dtos.cas_parts.cas_part_available_for import DDCASPartAvailableFor


class SSCASPart(HasClassLog):
    """ Holds information related to a CAS part. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_cas_part'

    def __init__(
        self,
        part_type: SSCASPartType,
        part_id: int,
        additional_part_ids: Tuple[int],
        display_name: LocalizedString,
        raw_display_name: str,
        author: str,
        available_for: DDCASPartAvailableFor,
        part_tags: Tuple[str],
        unique_identifier: Union[str, None]=None
    ):
        super().__init__()
        self._author_index = None
        self._cas_part_index = None
        self._part_type = part_type
        self._part_id = part_id
        self._additional_part_ids = additional_part_ids
        self._display_name = display_name or CommonLocalizationUtils.create_localized_string(raw_display_name)
        self._raw_display_name = raw_display_name
        self._author = author
        self._available_for = available_for
        self._tags = part_tags
        self._unique_identifier = unique_identifier

    @property
    def unique_identifier(self) -> str:
        """ An identifier that identifies the CAS part in a unique way. """
        if not self._unique_identifier:
            self._unique_identifier = '{}{}'.format(self.author, self.name)
            self._unique_identifier = ''.join((ch for ch in self._unique_identifier if ch.isalnum()))
        return self._unique_identifier

    @property
    def part_type(self) -> SSCASPartType:
        """ The type of the CAS Part. """
        return self._part_type

    @property
    def part_id(self) -> int:
        """ Decimal CAS Part Identifier of the CAS part. """
        return self._part_id

    @property
    def additional_part_ids(self) -> Tuple[int]:
        """ A collection of decimal identifier for additional CAS parts to equip when this CAS Part is equipped. """
        return self._additional_part_ids

    @property
    def name(self) -> str:
        """ The name of the CAS Part. """
        return str(self.raw_display_name or self.display_name)

    @property
    def display_name(self) -> LocalizedString:
        """ The string display name of the CAS part. """
        return self._display_name

    @property
    def display_name_hash(self) -> int:
        """ The display name as hash. """
        return CommonLocalizationUtils.get_localized_string_hash(self.display_name)

    @property
    def raw_display_name(self) -> str:
        """ The raw text display name of the CAS part. """
        return self._raw_display_name

    @property
    def author(self) -> str:
        """ Author of the CAS part. """
        return self._author

    @property
    def author_index(self) -> int:
        """ The index of the author used for sorting. """
        return self._author_index

    @author_index.setter
    def author_index(self, value: int):
        self._author_index = value

    @property
    def cas_part_index(self) -> int:
        """ The index of the cas part used for sorting. """
        return self._cas_part_index

    @cas_part_index.setter
    def cas_part_index(self, value: int):
        self._cas_part_index = value

    @property
    def available_for(self) -> DDCASPartAvailableFor:
        """ Information on what this part is available for. """
        return self._available_for

    @property
    def tags(self) -> Tuple[str]:
        """ Tags of the CAS part. """
        return self._tags

    @property
    def tag_list(self) -> Tuple[str]:
        """ A collection of tags for the CAS part. """
        tags = list()
        tags.append(self.author)
        for gender in self.available_for.genders:
            split = str(gender).split('.')
            tags.append(split[len(split) - 1])
        for part_tag in self.tags:
            tags.append(str(part_tag))
        return tuple(tags)

    def is_available_for_sim(self, sim_info: SimInfo) -> bool:
        """ Determine if the CAS part is available for a sim. """
        age = CommonAgeUtils.get_age(sim_info)
        if age not in self.available_for.ages:
            return False
        gender = CommonGenderUtils.get_gender(sim_info)
        if gender not in self.available_for.genders:
            return False
        common_species = CommonSpecies.get_species(sim_info)
        if common_species not in self.available_for.species:
            return False
        return True

    def is_valid(self) -> Tuple[bool, str]:
        """ Determine if the CAS part is valid or not. """
        if self.part_type == SSCASPartType.NONE:
            return False, 'CAS Part Type was NONE'
        if self.part_id == -1:
            return False, 'Part Id was -1'
        if self.raw_display_name is None and self.display_name is None:
            return False, 'No display name was specified.'
        if not CommonCASUtils.is_cas_part_loaded(self.part_id):
            return False, 'CAS Part is not loaded.'
        (available_for_result, available_for_reason) = self.available_for.is_valid()
        if not available_for_result:
            return False, 'Available For was invalid. Reason: {}'.format(available_for_reason)
        return True, 'Success'

    def __eq__(self, other: 'SSCASPart') -> bool:
        if not isinstance(other, SSCASPart):
            return False
        return self.part_id == other.part_id

    def __hash__(self) -> int:
        return hash((str(self.part_id), str(self.part_type)))

    def __repr__(self) -> str:
        return '<name:{}\nunique_identifier: {}\nauthor:{}\npart_id:{}\npart_tags:{}\navailable_for:{}>'\
            .format(self.name, self.unique_identifier, self.author, self.part_id, self.tags, str(self.available_for))

    def __str__(self) -> str:
        return '\'{}\' by \'{}\''.format(self.name, self.author)
