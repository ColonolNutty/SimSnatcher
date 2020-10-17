"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Set

from cnsimsnatcher.modinfo import ModInfo
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_persisted_sim_data_storage import CommonPersistedSimDataStorage
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSSimDataStore(CommonPersistedSimDataStorage):
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
    def slave_sim_ids(self) -> Set[int]:
        """ Slaves this Sim owns """
        return self.get_data(default=set())

    @slave_sim_ids.setter
    def slave_sim_ids(self, value: Set[int]):
        self.set_data(value)

    @property
    def captive_sim_ids(self) -> Set[int]:
        """ Captives this Sim has captured. """
        return self.get_data(default=set())

    @captive_sim_ids.setter
    def captive_sim_ids(self, value: Set[int]):
        self.set_data(value)

    @property
    def allowances(self) -> Set[CommonGameTag]:
        """ Retrieve the allowances for the Sim. """
        return self.get_data(default=set())

    @allowances.setter
    def allowances(self, value: Set[CommonGameTag]):
        self.set_data(value)


@Command('ss.print_sim_data', command_type=CommandType.Live)
def _ss_command_print_sim_data(_connection: int=None):
    output = CheatOutput(_connection)
    sim_info = CommonSimUtils.get_active_sim_info()
    output('Sim Data for Sim: Name: \'{}\' Id: \'{}\''.format(CommonSimNameUtils.get_full_name(sim_info), CommonSimUtils.get_sim_id(sim_info)))
    sim_storage = SSSimDataStore(sim_info)
    for (key, value) in sim_storage._data.items():
        output(' > {}: {}'.format(pformat(key), pformat(value)))
