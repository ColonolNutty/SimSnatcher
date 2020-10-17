"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Tuple, Callable, List, Union

from cnsimsnatcher.configuration.allowance.utils.allowance_utils import SSAllowanceUtils
from cnsimsnatcher.enums.trait_ids import SSTraitId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.persistence.ss_sim_data_storage import SSSimDataStore
from cnsimsnatcher.slavery.enums.interaction_ids import SSSlaveryInteractionId
from cnsimsnatcher.slavery.enums.relationship_bit_ids import SSSlaveryRelationshipBitId
from cnsimsnatcher.slavery.enums.situation_ids import SSSlaverySituationId
from cnsimsnatcher.slavery.enums.trait_ids import SSSlaveryTraitId
from cnsimsnatcher.utils.buff_utils import SSBuffUtils
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_situation_utils import CommonSimSituationUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ssutilities.commonlib.utils.common_situation_utils import SSCommonSituationUtils


class SSSlaveryStateUtils(HasLog):
    """ Utilities for managing Slavery state. """
    def __init__(self) -> None:
        super().__init__()
        self._buff_utils = SSBuffUtils()

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
        master_data_store = SSSimDataStore(master_sim_info)
        if not master_data_store.slave_sim_ids:
            return False
        for slave_sim_id in master_data_store.slave_sim_ids:
            if instanced_only and CommonSimUtils.get_sim_instance(slave_sim_id) is None:
                continue
            return True
        return False

    def has_master(self, slave_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has any Masters. """
        slave_data_store = SSSimDataStore(slave_sim_info)
        if slave_data_store.master_sim_id == -1:
            return False
        if instanced_only and CommonSimUtils.get_sim_instance(slave_data_store.master_sim_id) is None:
            return False
        return True

    def is_master_of(self, master_sim_info: SimInfo, slave_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is a Master of another Sim. """
        slave_data_store = SSSimDataStore(slave_sim_info)
        if slave_data_store.master_sim_id == -1:
            return False
        master_sim_id = CommonSimUtils.get_sim_id(master_sim_info)
        return slave_data_store.master_sim_id == master_sim_id

    def is_slave_of(self, slave_sim_info: SimInfo, master_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is a Slave of another Sim. """
        master_data_store = SSSimDataStore(master_sim_info)
        if not master_data_store.slave_sim_ids:
            return False
        slave_sim_id = CommonSimUtils.get_sim_id(slave_sim_info)
        return slave_sim_id in master_data_store.slave_sim_ids

    def get_slaves(self, master_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """get_slaves(master_sim_info, instanced_only=True)

        Retrieve a collection of Sims that are a Slave to the specified Sim.

        :param master_sim_info: An instance of a Sim.
        :type master_sim_info: SimInfo
        :param instanced_only: If True, only Slaves that are currently loaded will be retrieved. If False, all Slaves, including those not loaded will be retrieved. Default is True.
        :type instanced_only: bool, optional
        :return: A collection of Sims the specified Sim has Enslaved.
        :rtype: Tuple[SimInfo]
        """
        master_data_store = SSSimDataStore(master_sim_info)
        slaves: List[SimInfo] = list()
        for slave_sim_id in master_data_store.slave_sim_ids:
            slave_sim_info = CommonSimUtils.get_sim_info(slave_sim_id)
            if instanced_only and CommonSimUtils.get_sim_instance(slave_sim_info) is None:
                continue
            slaves.append(slave_sim_info)
        return tuple(slaves)

    def get_master(self, slave_sim_info: SimInfo, instanced_only: bool=True) -> Union[SimInfo, None]:
        """ Retrieve a collection of Sims that are a Master of the specified Sim. """
        slave_data_store = SSSimDataStore(slave_sim_info)
        master_sim_id = slave_data_store.master_sim_id
        if instanced_only and CommonSimUtils.get_sim_instance(master_sim_id) is None:
            return None
        return CommonSimUtils.get_sim_info(master_sim_id)

    def get_all_masters(self, include_sim_callback: Callable[[SimInfo], bool]=None, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve a collection of Sims that are Masters of Slaves and are part of the active household. """
        _has_slaves = CommonFunctionUtils.run_predicates_as_one(
            (
                include_sim_callback,
                CommonFunctionUtils.run_with_arguments(
                    self.has_slaves,
                    instanced_only=False
                )
            )
        )
        if instanced_only:
            return tuple(CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=_has_slaves))
        else:
            return tuple(CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=_has_slaves))

    def refresh_slave(self, slave_sim_info: SimInfo) -> bool:
        """refresh_slave(slave_sim_info)

        Refresh the state of a Slave Sim.

        :param slave_sim_info: The Sim to refresh the state of.
        :type slave_sim_info: SimInfo
        :return: True, if the Sim was turned into a Slave successfully. False, if not.
        :rtype: bool
        """
        CommonTraitUtils.remove_trait(slave_sim_info, SSTraitId.PREVENT_LEAVE)
        CommonTraitUtils.add_trait(slave_sim_info, SSTraitId.PREVENT_LEAVE)
        CommonTraitUtils.remove_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)
        CommonTraitUtils.add_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)
        return True

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
        slave_sim_id = CommonSimUtils.get_sim_id(slave_sim_info)
        master_sim_name = CommonSimNameUtils.get_full_name(master_sim_info)
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
            self._buff_utils.remove_appropriateness_related_buffs(slave_sim_info)
            CommonTraitUtils.add_trait(slave_sim_info, SSTraitId.PREVENT_LEAVE)
            CommonTraitUtils.add_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)
            slave_data_store = SSSimDataStore(slave_sim_info)
            master_sim_id = CommonSimUtils.get_sim_id(master_sim_info)
            slave_data_store.master_sim_id = master_sim_id
            master_data_store = SSSimDataStore(master_sim_info)
            if slave_sim_id not in master_data_store.slave_sim_ids:
                master_data_store.slave_sim_ids.add(slave_sim_id)
            slave_data_store.owning_household_id = CommonHouseholdUtils.get_household_id(master_sim_info)
            SSAllowanceUtils().set_allow_all(slave_sim_info)
            CommonSimInteractionUtils.cancel_all_queued_or_running_interactions(slave_sim_info, cancel_reason='Became a Slave')
        except Exception as ex:
            self.log.error('Problem occurred while creating Slave \'{}\' with Master \'{}\'.'.format(slave_sim_name, master_sim_name), exception=ex)
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
        slave_sim_id = CommonSimUtils.get_sim_id(slave_sim_info)
        try:
            self.log.debug('Attempting to release Slave \'{}\'.'.format(slave_sim_name))
            slave_data_store = SSSimDataStore(slave_sim_info)
            master_sim_info = self.get_master(slave_sim_info, instanced_only=False)
            if master_sim_info is not None:
                master_sim_name = CommonSimNameUtils.get_full_name(master_sim_info)

                master_data_store = SSSimDataStore(master_sim_info)
                if slave_sim_id in master_data_store.slave_sim_ids:
                    master_data_store.slave_sim_ids.remove(slave_sim_id)
                self.log.debug('Attempting to remove relationship bits between Master \'{}\' and Slave \'{}\'.'.format(master_sim_name, slave_sim_name))
                CommonRelationshipUtils.remove_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.MASTER_SIM_TO_SLAVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.SIM_IS_MASTER_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(master_sim_info, slave_sim_info, SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(slave_sim_info, master_sim_info, SSSlaveryRelationshipBitId.SIM_IS_SLAVE_OF_SIM_REL_BIT)
                self.log.debug('Done removing relationship bits between Master \'{}\' and Slave \'{}\'.'.format(master_sim_name, slave_sim_name))
                self.log.debug('Done removing Master relationships.')

            slave_data_store.master_sim_id = -1
            self.log.debug('Attempting to remove traits.')
            CommonTraitUtils.remove_trait(slave_sim_info, SSSlaveryTraitId.SLAVE)
            self.log.debug('Attempting to remove buffs.')
            CommonTraitUtils.remove_trait(slave_sim_info, SSTraitId.PREVENT_LEAVE)
            SSAllowanceUtils().set_disallow_all(slave_sim_info)
            slave_data_store.owning_household_id = -1
            self.log.debug('Done removing buffs.')
            self.log.debug('Attempting to remove situations.')
            SSCommonSituationUtils.remove_sim_from_situation(slave_sim_info, SSSlaverySituationId.NPC_ENSLAVED_BY_PLAYER)
            self.log.debug('Done removing sim from situations.')
            if not CommonSimTypeUtils.is_player_sim(slave_sim_info):
                self.log.debug('Attempting to make Sim leave.')
                SSCommonSituationUtils.make_sim_leave(slave_sim_info)
                self.log.debug('Done making Sim leave.')
            self.log.debug('Done releasing Slave \'{}\'.'.format(slave_sim_name))
        except Exception as ex:
            self.log.error('Problem occurred while releasing Slave \'{}\'.'.format(slave_sim_name), exception=ex)
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
        return self.has_master(slave_sim_info)\
               and (not CommonSimSituationUtils.has_situations(slave_sim_info, (SSSlaverySituationId.NPC_ENSLAVED_BY_PLAYER, ))
                    or not CommonTraitUtils.has_trait(slave_sim_info, SSSlaveryTraitId.SLAVE))\
               and not CommonSimInteractionUtils.has_interaction_running_or_queued(slave_sim_info, SSSlaveryInteractionId.ATTEMPT_TO_ENSLAVE_HUMAN_SUCCESS_OUTCOME)


@sims4.commands.Command('ss.show_slaves', command_type=sims4.commands.CommandType.Live)
def _ss_slavery_show_slaves(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing slaves of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    sim_info_list = SSSlaveryStateUtils().get_slaves(active_sim_info, instanced_only=False)
    if not sim_info_list:
        output('No slaves were found for the Active Sim.')
    else:
        for sim_info in sim_info_list:
            output('\'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    output('Done displaying slaves.')


@sims4.commands.Command('ss.show_master', command_type=sims4.commands.CommandType.Live)
def _ss_slavery_show_master(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing master of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    master_sim_info = SSSlaveryStateUtils().get_master(active_sim_info, instanced_only=False)
    if not master_sim_info:
        output('No master was found for the Active Sim.')
    else:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(master_sim_info)))
    output('Done displaying master.')
