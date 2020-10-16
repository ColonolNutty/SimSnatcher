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
    def is_slave(self) -> bool:
        """ Whether this Sim is a slave or not. """
        return self.get_data(default=False)

    @is_slave.setter
    def is_slave(self, value: bool):
        self.set_data(value)

    @property
    def is_captive(self) -> bool:
        """ Whether this Sim is a captive or not. """
        return self.get_data(default=False)

    @is_captive.setter
    def is_captive(self, value: bool):
        self.set_data(value)

    @property
    def allowances(self) -> Set[CommonGameTag]:
        """ Retrieve the allowances for the Sim. """
        from cnsimsnatcher.configuration.allowance.utils.allowance_utils import SSAllowanceUtils
        return self.get_data(default=SSAllowanceUtils().get_appropriateness_tags(self.sim_info))

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
