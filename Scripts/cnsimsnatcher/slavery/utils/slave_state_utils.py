"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from cnsimsnatcher.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class SSSlaveStateUtils(HasLog):
    """ Utilities for controlling Slave state. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_slave_state_utils'

    def is_slave(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim is a Slave or not. """
        return False

    def is_slave_of(self, slave_sim_info: SimInfo, master_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is the Slave of the Target Sim. """
        return self.is_master_of(master_sim_info, slave_sim_info)

    def is_master_of(self, master_sim_info: SimInfo, slave_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is the Master of the Target Sim. """
        return False

    def convert_hostage_to_slave(self, hostage_sim_info: SimInfo) -> bool:
        """ Convert a Hostage Sim to a Slave Sim. """
        return False

    def create_slave(self, slave_sim_info: SimInfo, master_sim_info: SimInfo) -> Tuple[bool, str]:
        """create_slave(slave_sim_info, master_sim_info)

        Turn a Sim into a Slave.

        :param slave_sim_info: The Sim to turn into a Slave.
        :type slave_sim_info: SimInfo
        :param master_sim_info: The Sim that will be the Master of the Slave.
        :type master_sim_info: SimInfo
        :return: True, if the Sim was turned into a Slave successfully. False, if not.
        :rtype: bool
        """
        slave_sim_name = CommonSimNameUtils.get_full_name(slave_sim_info)
        if slave_sim_info is master_sim_info:
            return False, 'Failed, \'{}\' cannot be a Slave to themselves.'.format(slave_sim_name)
        return False, 'Failed to turn \'{}\' into a Slave for unknown reasons.'.format(slave_sim_name)

    def release_slave(self, slave_sim_info: SimInfo, releasing_sim_info: SimInfo=None) -> bool:
        """release_slave(slave_sim_info, releasing_sim_info=None)

        Release a Slave Sim from Indentured Servitude.

        :param slave_sim_info: The Slave being released.
        :type slave_sim_info: SimInfo
        :param releasing_sim_info: The Sim that is releasing the Slave. Default is None.
        :type releasing_sim_info: SimInfo, optional
        :return: True, if the Slave was released successfully. False, if not.
        :rtype: bool
        """
        return False
