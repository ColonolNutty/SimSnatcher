"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from sims.outfits.outfit_enums import BodyType
from sims.sim_info_types import Gender, Age
from sims4.localization import TunableLocalizedString
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import Tunable, TunableList, HasTunableFactory, AutoFactoryInit,\
    TunableEnumEntry, TunableEnumSet, TunableSet
from sims4.tuning.tunable_base import GroupNames
from sims4communitylib.enums.common_species import CommonSpecies
from cnsimsnatcher.bindings.enums.binding_body_location import SSBindingBodyLocation


class _SimSnatcherCASPartData(HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        'part_id': Tunable(tunable_type=int, default=0),
        'additional_part_ids': TunableSet(tunable=Tunable(tunable_type=int, default=0)),
        'part_display_name': TunableLocalizedString(default=None),
        'part_raw_display_name': Tunable(tunable_type=str, default=''),
        'part_author': Tunable(tunable_type=str, default=''),
        'part_tags': TunableSet(tunable=Tunable(tunable_type=str, default=None), tuning_group=GroupNames.TAG),
        'available_for_genders': TunableEnumSet(enum_type=Gender, default_enum_list=(Gender.MALE, Gender.FEMALE)),
        'available_for_ages': TunableEnumSet(enum_type=Age, default_enum_list=(Age.TEEN, Age.YOUNGADULT, Age.ADULT, Age.ELDER)),
        'available_for_species': TunableEnumSet(enum_type=CommonSpecies, default_enum_list=(CommonSpecies.HUMAN,)),
    }

    __slots__ = [
        'part_id',
        'additional_part_ids',
        'part_display_name',
        'part_raw_display_name',
        'part_author',
        'part_tags',
        'available_for_genders',
        'available_for_ages',
        'available_for_species'
    ]


class _SimSnatcherBindingCASPartData(_SimSnatcherCASPartData):
    FACTORY_TUNABLES = {
        'part_display_icon': Tunable(tunable_type=int, default=0),
        'body_location': TunableEnumEntry(tunable_type=SSBindingBodyLocation, default=SSBindingBodyLocation.NONE)
    }

    __slots__ = [
        'part_type',
        'part_display_icon',
        'body_location',
        'part_id',
        'additional_part_ids',
        'part_display_name',
        'part_raw_display_name',
        'part_author',
        'part_tags',
        'available_for_genders',
        'available_for_ages',
        'available_for_species'
    ]


class _SimSnatcherBodyCASPartData(_SimSnatcherCASPartData):
    FACTORY_TUNABLES = {
        'part_body_type': TunableEnumEntry(tunable_type=BodyType, default=BodyType.NONE)
    }

    __slots__ = [
        'part_type',
        'part_body_type',
        'part_id',
        'additional_part_ids',
        'part_display_name',
        'part_raw_display_name',
        'part_author',
        'part_tags',
        'available_for_genders',
        'available_for_ages',
        'available_for_species'
    ]


class _SimSnatcherCASPartPackage(metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'has_sim_snatcher_cas_parts': Tunable(tunable_type=bool, default=True),
        'binding_cas_parts_list': TunableList(tunable=_SimSnatcherBindingCASPartData.TunableFactory()),
        'body_cas_parts_list': TunableList(tunable=_SimSnatcherBodyCASPartData.TunableFactory()),
    }

    __slots__ = [
        'has_sim_snatcher_cas_parts',
        'binding_cas_parts_list',
        'body_cas_parts_list',
    ]


SimSnatcherCASPartData = _SimSnatcherCASPartData
SimSnatcherBindingCASPartData = _SimSnatcherBindingCASPartData
SimSnatcherBodyCASPartData = _SimSnatcherBodyCASPartData
SimSnatcherCASPartPackage = _SimSnatcherCASPartPackage
