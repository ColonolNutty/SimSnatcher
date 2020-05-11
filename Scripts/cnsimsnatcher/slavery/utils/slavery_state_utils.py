"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Tuple

from cnsimsnatcher.enums.buff_ids import SSBuffId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.enums.interaction_ids import SSSlaveryInteractionId
from cnsimsnatcher.slavery.enums.relationship_bit_ids import SSSlaveryRelationshipBitId
from cnsimsnatcher.slavery.enums.situation_ids import SSSlaverySituationId
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from cnsimsnatcher.slavery.enums.trait_ids import SSSlaveryTraitId
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ssutilities.commonlib.utils.common_situation_utils import CommonSituationUtils


class SSSlaveryStateUtils(HasLog):
    """ Utilities for managing Slavery state. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_slave_state_utils'

    def has_slaves(self, master_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has any Slaves. """
        return CommonRelationshipUtils.has_relationship_bit_with_any_sims(
            master_sim_info,
            SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT,
            instanced_only=instanced_only
        )

    def has_masters(self, slave_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has any Masters. """
        return CommonTraitUtils.has_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)\
               or CommonRelationshipUtils.has_relationship_bit_with_any_sims(
            slave_sim_info,
            SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT,
            instanced_only=instanced_only
        )

    def is_slave_of(self, slave_sim_info: SimInfo, master_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is a Slave of another Sim. """
        from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
        return CommonRelationshipUtils.has_relationship_bit_with_sim(
            slave_sim_info,
            master_sim_info,
            SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT
        )\
               and CommonRelationshipUtils.has_relationship_bit_with_sim(
            slave_sim_info,
            master_sim_info,
            SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT
        )

    def is_master_of(self, master_sim_info: SimInfo, slave_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is a Master of another Sim. """
        from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
        return CommonRelationshipUtils.has_relationship_bit_with_sim(
            master_sim_info,
            slave_sim_info,
            SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT
        )\
               and CommonRelationshipUtils.has_relationship_bit_with_sim(
            master_sim_info,
            slave_sim_info,
            SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT
        )

    def get_slaves(self, master_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve a collection of Sims that are a Slave to the specified Sim. """
        return tuple(
            CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(
                master_sim_info,
                SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT,
                instanced_only=instanced_only
            )
        )

    def get_masters(self, slave_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve a collection of Sims that are a Master of the specified Sim. """
        return tuple(
            CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(
                slave_sim_info,
                SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT,
                instanced_only=instanced_only
            )
        )

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
        if slave_sim_info is None or master_sim_info is None:
            return False, 'Failed, missing Slave or Master data.'
        slave_sim_name = CommonSimNameUtils.get_full_name(slave_sim_info)
        try:
            if slave_sim_info is master_sim_info:
                return False, 'Failed, \'{}\' cannot be a Slave to themselves.'.format(slave_sim_name)
            from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
            if not SSAbductionStateUtils().release_captive(slave_sim_info):
                return False, 'Failed, failed to clear abduction data before converting \'{}\' to Slave.'.format(CommonSimNameUtils.get_full_name(slave_sim_info))
            if not CommonRelationshipUtils.has_met(master_sim_info, slave_sim_info) and not CommonRelationshipUtils.add_relationship_bit(master_sim_info, slave_sim_info, CommonRelationshipBitId.HAS_MET):
                self.log.error('Failed to add Has Met Relationship Bit.')
            if not CommonRelationshipUtils.add_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT):
                self.log.error('Failed to add Master/Slave Relationship Bit.')
            if not CommonRelationshipUtils.add_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT):
                self.log.error('Failed to add Master Relationship Bit.')
            if not CommonRelationshipUtils.add_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT):
                self.log.error('Failed to add Slave Relationship Bit.')
            CommonBuffUtils.add_buff(slave_sim_info, SSBuffId.ALLOWED_NOTHING_INVISIBLE, buff_reason=CommonLocalizationUtils.create_localized_string(SSSlaveryStringId.BEING_ENSLAVED))
            CommonBuffUtils.add_buff(slave_sim_info, SSBuffId.PREVENT_LEAVE_INVISIBLE, buff_reason=CommonLocalizationUtils.create_localized_string(SSSlaveryStringId.BEING_ENSLAVED))
            CommonTraitUtils.add_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred while creating Slave \'{}\'.'.format(slave_sim_name), exception=ex)
            return False, 'Failed, Exception Occurred.'
        return True, 'Success, \'{}\' is now a Slave.'.format(CommonSimNameUtils.get_full_name(slave_sim_info))

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
        if slave_sim_info is None:
            self.log.debug('slave_sim_info was None.')
            return False
        slave_sim_name = CommonSimNameUtils.get_full_name(slave_sim_info)
        try:
            self.log.debug('Attempting to release Slave \'{}\'.'.format(slave_sim_name))
            if releasing_sim_info is not None and self.is_slave_of(slave_sim_info, releasing_sim_info):
                master_sim_info_list = (releasing_sim_info,)
            else:
                master_sim_info_list = self.get_masters(slave_sim_info)

            for master_sim_info in master_sim_info_list:
                master_sim_name = CommonSimNameUtils.get_full_name(master_sim_info)
                self.log.debug('Attempting to remove relationship bits between Master \'{}\' and Slave \'{}\'.'.format(master_sim_name, slave_sim_name))
                CommonRelationshipUtils.remove_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT)
                self.log.debug('Done removing relationship bits between Master \'{}\' and Slave \'{}\'.'.format(master_sim_name, slave_sim_name))
            self.log.debug('Done removing Master relationships.')

            self.log.debug('Attempting to remove traits.')
            CommonTraitUtils.remove_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)
            self.log.debug('Attempting to remove buffs.')
            CommonBuffUtils.remove_buff(slave_sim_info, SSBuffId.ALLOWED_NOTHING_INVISIBLE)
            CommonBuffUtils.remove_buff(slave_sim_info, SSBuffId.PREVENT_LEAVE_INVISIBLE)
            self.log.debug('Done removing buffs.')
            self.log.debug('Attempting to remove situations.')
            CommonSituationUtils.remove_sim_from_situation(slave_sim_info, SSSlaverySituationId.NPC_ENSLAVED_BY_PLAYER)
            self.log.debug('Done removing sim from situations.')
            self.log.debug('Making Sim leave.')
            CommonSituationUtils.make_sim_leave(slave_sim_info)
            self.log.debug('Made Sim leave.')
            self.log.debug('Done releasing Slave \'{}\'.'.format(slave_sim_name))
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred while releasing Slave \'{}\'.'.format(slave_sim_name), exception=ex)
            return False
        return True

    def release_slaves_of(self, master_sim_info: SimInfo) -> bool:
        """release_slaves_of(master_sim_info)

        Release all Slaves of the specified Master Sim.

        :param master_sim_info: The Master Sim to release the Slaves of.
        :type master_sim_info: SimInfo
        :return: True, if all Slaves of the specified Master Sim were released successfully. False, if not.
        :rtype: bool
        """
        if master_sim_info is None:
            self.log.debug('master_sim_info was None.')
            return False
        master_sim_name = CommonSimNameUtils.get_full_name(master_sim_info)
        self.log.debug('Releasing All Slaves of Master \'{}\'.'.format(master_sim_name))
        slave_sim_info_list = self.get_slaves(master_sim_info)
        for slave_sim_info in slave_sim_info_list:
            self.release_slave(slave_sim_info, releasing_sim_info=master_sim_info)
        self.log.debug('Done releasing all Slaves of Master \'{}\'.'.format(master_sim_info))
        return True

    def has_invalid_enslaved_state(self, slave_sim_info: SimInfo) -> bool:
        """ Determine if a Sim has an invalid enslaved state. """
        return self.has_masters(slave_sim_info)\
               and (not CommonSituationUtils.has_situation(slave_sim_info, SSSlaverySituationId.NPC_ENSLAVED_BY_PLAYER)
                    or not CommonTraitUtils.has_trait(slave_sim_info, SSSlaveryTraitId.SLAVE))\
               and not CommonSimInteractionUtils.has_interaction_running_or_queued(slave_sim_info, SSSlaveryInteractionId.ATTEMPT_TO_ENSLAVE_HUMAN_SUCCESS_OUTCOME)


@sims4.commands.Command('simsnatcher.show_slaves', command_type=sims4.commands.CommandType.Live)
def _ss_slavery_show_slaves_names(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing slaves of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    sim_info_list = SSSlaveryStateUtils().get_slaves(active_sim_info)
    for sim_info in sim_info_list:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    output('Done displaying slaves.')


@sims4.commands.Command('simsnatcher.show_masters', command_type=sims4.commands.CommandType.Live)
def _ss_slavery_show_master_names(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing masters of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    sim_info_list = SSSlaveryStateUtils().get_masters(active_sim_info)
    for sim_info in sim_info_list:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    output('Done displaying masters.')
