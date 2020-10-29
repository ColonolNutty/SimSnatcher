"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, Dict

from cnsimsnatcher.bindings.enums.binding_body_location import SSBindingBodyLocation
from cnsimsnatcher.bindings.enums.body_side import SSBodySide
from cnsimsnatcher.modinfo import ModInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_persisted_sim_data_storage import CommonPersistedSimDataStorage
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSSimData(CommonPersistedSimDataStorage):
    """ Sim data storage """
    # noinspection PyMissingOrEmptyDocstring,PyMethodParameters
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_sim_data'

    @property
    def owning_household_id(self) -> int:
        """ The identifier of the household that owns this Sim """
        return int(self.get_data(default=-1))

    @owning_household_id.setter
    def owning_household_id(self, value: int):
        self.set_data(value)

    @property
    def captor_household_id(self) -> int:
        """ The identifier of the household that has captured this Sim """
        return int(self.get_data(default=-1))

    @captor_household_id.setter
    def captor_household_id(self, value: int):
        self.set_data(value)

    @property
    def is_slave(self) -> bool:
        """ Determine if this Sim is a slave or not. """
        return self.master_sim_id != -1

    @property
    def is_captive(self) -> bool:
        """ Determine if this Sim is a captive or not. """
        return self.captor_sim_id != -1

    @property
    def is_slave_or_captive(self) -> bool:
        """ Determine if this Sim is a Slave or Captive or not. """
        return self.is_slave or self.is_captive

    @property
    def is_master(self) -> bool:
        """ Determine if this Sim is a master of slaves or not. """
        return len(self.slave_sim_ids) > 0

    @property
    def is_captor(self) -> bool:
        """ Determine if this Sim has captives or not. """
        return len(self.captive_sim_ids) > 0

    @property
    def master_sim_id(self) -> int:
        """ Master of this Sim. """
        return int(self.get_data(default=-1))

    @master_sim_id.setter
    def master_sim_id(self, value: int):
        self.set_data(value)

    @property
    def captor_sim_id(self) -> int:
        """ Captor of this Sim. """
        return int(self.get_data(default=-1))

    @captor_sim_id.setter
    def captor_sim_id(self, value: int):
        self.set_data(value)

    @property
    def slave_sim_ids(self) -> Tuple[int]:
        """ Slaves this Sim owns """
        return self.get_data(default=tuple())

    @slave_sim_ids.setter
    def slave_sim_ids(self, value: Tuple[int]):
        self.set_data(value)

    @property
    def captive_sim_ids(self) -> Tuple[int]:
        """ Captives this Sim has captured. """
        return self.get_data(default=tuple())

    @captive_sim_ids.setter
    def captive_sim_ids(self, value: Tuple[int]):
        self.set_data(value)

    @property
    def allowances(self) -> Tuple[CommonGameTag]:
        """ Current things the Sim is allowed to do. """
        return self.get_data(default=tuple())

    @allowances.setter
    def allowances(self, value: Tuple[CommonGameTag]):
        self.set_data(value)

    @property
    def restrained_body_parts(self) -> Dict[str, SSBodySide]:
        """ Body parts currently being restrained on a Sim organized by SSBindingBodyLocation. """
        return self.get_data(default=dict())

    @restrained_body_parts.setter
    def restrained_body_parts(self, value: Dict[str, SSBodySide]):
        self.set_data(value)

    def has_body_restraint(self, location: SSBindingBodyLocation, body_side: SSBodySide):
        """ Determine if a body restraint has been applied. """
        if location.name not in self.restrained_body_parts:
            return False
        current_restraint = self.restrained_body_parts[location.name]
        if current_restraint == body_side:
            return True
        if current_restraint == SSBodySide.BOTH:
            return True
        return False

    def apply_body_restraint(self, location: SSBindingBodyLocation, body_side: SSBodySide):
        """ Apply a body restraint. """
        if location.name in self.restrained_body_parts:
            current_restraint = self.restrained_body_parts[location.name]
            if current_restraint == SSBodySide.BOTH:
                return
            if current_restraint == SSBodySide.RIGHT and body_side == SSBodySide.LEFT:
                body_side = SSBodySide.BOTH
            elif current_restraint == SSBodySide.LEFT and body_side == SSBodySide.RIGHT:
                body_side = SSBodySide.BOTH
        # noinspection PyAttributeOutsideInit
        self.restrained_body_parts[location.name] = body_side

    def remove_body_restraint(self, location: SSBindingBodyLocation, body_side: SSBodySide):
        """ Remove a body restraint. """
        if location.name not in self.restrained_body_parts:
            return
        current_restraint = self.restrained_body_parts[location.name]
        if current_restraint == body_side or body_side == SSBodySide.BOTH:
            del self.restrained_body_parts[location.name]
            return
        if current_restraint == SSBodySide.BOTH:
            if body_side == SSBodySide.RIGHT:
                body_side = SSBodySide.LEFT
            elif body_side == SSBodySide.LEFT:
                body_side = SSBodySide.RIGHT
        self.restrained_body_parts[location.name] = body_side


@Command('ss.print_sim_data', command_type=CommandType.Live)
def _ss_command_print_sim_data(_connection: int=None):
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    output('Sim Data for Sim: Name: \'{}\' Id: \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info), CommonSimUtils.get_sim_id(sim_info)))
    sim_storage = SSSimData(sim_info)
    for (key, value) in sim_storage._data.items():
        output(' > {}: {}'.format(pformat(key), pformat(value)))
