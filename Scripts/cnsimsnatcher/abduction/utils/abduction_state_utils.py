"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Callable, List, Union
import sims4.commands
from cnsimsnatcher.abduction.enums.interaction_ids import SSAbductionInteractionId
from cnsimsnatcher.abduction.enums.relationship_bit_ids import SSAbductionRelationshipBitId
from cnsimsnatcher.abduction.enums.situation_ids import SSAbductionSituationId
from cnsimsnatcher.abduction.enums.trait_ids import SSAbductionTraitId
from cnsimsnatcher.configuration.allowance.utils.allowance_utils import SSAllowanceUtils
from cnsimsnatcher.enums.trait_ids import SSTraitId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.persistence.ss_sim_data import SSSimData
from cnsimsnatcher.utils.buff_utils import SSBuffUtils
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.utils.sims.common_sim_situation_utils import CommonSimSituationUtils
from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ssutilities.commonlib.utils.common_situation_utils import SSCommonSituationUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSAbductionStateUtils(HasLog):
    """ Utilities for managing Abduction state. """
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
        return 'ssa_state_utils'

    def has_captives(self, captor_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has captives. """
        captor_sim_data = SSSimData(captor_sim_info)
        if not captor_sim_data.captive_sim_ids:
            return False
        for captive_sim_id in captor_sim_data.captive_sim_ids:
            if instanced_only and CommonSimUtils.get_sim_instance(captive_sim_id) is None:
                continue
            return True
        return False

    def has_captor(self, captive_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has a Captor. """
        captive_sim_data = SSSimData(captive_sim_info)
        if captive_sim_data.captor_sim_id == -1:
            return False
        if instanced_only and CommonSimUtils.get_sim_instance(captive_sim_data.captor_sim_id) is None:
            return False
        return True

    def is_captor_of(self, captor_sim_info: SimInfo, captive_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is the Captor of the specified Sim. """
        captive_sim_data = SSSimData(captive_sim_info)
        if captive_sim_data.captor_sim_id == -1:
            return False
        captor_sim_id = CommonSimUtils.get_sim_id(captor_sim_info)
        return captive_sim_data.captor_sim_id == captor_sim_id

    def is_captive_of(self, captive_sim_info: SimInfo, captor_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is a Captive of the specified Sim. """
        captor_sim_data = SSSimData(captor_sim_info)
        if not captor_sim_data.captive_sim_ids:
            return False
        captive_sim_id = CommonSimUtils.get_sim_id(captive_sim_info)
        return captive_sim_id in captor_sim_data.captive_sim_ids

    def get_captives(self, captor_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """get_captives(captor_sim_info, instanced_only=True)

        Retrieve a collection of Sims that are a Captive to the specified Sim.

        :param captor_sim_info: An instance of a Sim.
        :type captor_sim_info: SimInfo
        :param instanced_only: If True, only Captives that are currently loaded will be retrieved. If False, all Captives, including those not loaded will be retrieved. Default is True.
        :type instanced_only: bool, optional
        :return: A collection of Sims the specified Sim has Captured.
        :rtype: Tuple[SimInfo]
        """
        captor_sim_data = SSSimData(captor_sim_info)
        captives: List[SimInfo] = list()
        for captive_sim_id in captor_sim_data.captive_sim_ids:
            captive_sim_info = CommonSimUtils.get_sim_info(captive_sim_id)
            if instanced_only and CommonSimUtils.get_sim_instance(captive_sim_info) is None:
                continue
            captives.append(captive_sim_info)
        return tuple(captives)

    def get_captor(self, captive_sim_info: SimInfo, instanced_only: bool=True) -> Union[SimInfo, None]:
        """ Retrieve a collection of Sims that are a Captor of the specified Sim. """
        captive_sim_data = SSSimData(captive_sim_info)
        captor_sim_id = captive_sim_data.captor_sim_id
        if instanced_only and CommonSimUtils.get_sim_instance(captor_sim_id) is None:
            return None
        return CommonSimUtils.get_sim_info(captor_sim_id)

    def get_all_captors(self, include_sim_callback: Callable[[SimInfo], bool]=None, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve a collection of Sims that are Captors of Captives. """
        _has_captives = CommonFunctionUtils.run_predicates_as_one(
            (
                include_sim_callback,
                CommonFunctionUtils.run_with_arguments(
                    self.has_captives,
                    instanced_only=False
                )
            )
        )
        if instanced_only:
            return tuple(CommonSimUtils.get_instanced_sim_info_for_all_sims_generator(include_sim_callback=_has_captives))
        else:
            return tuple(CommonSimUtils.get_sim_info_for_all_sims_generator(include_sim_callback=_has_captives))

    def create_captive(self, captive_sim_info: SimInfo, captor_sim_info: SimInfo) -> Tuple[bool, str]:
        """create_captive(captive_sim_info, captor_sim_info)

        Turn a Sim into a Captive.

        :param captive_sim_info: The Sim to turn into a Captive.
        :type captive_sim_info: SimInfo
        :param captor_sim_info: The Sim that will be the Captor of the Captive.
        :type captor_sim_info: SimInfo
        :return: True, if the Sim was turned into a Captive successfully. False, if not.
        :rtype: bool
        """
        if captive_sim_info is None or captor_sim_info is None:
            return False, 'Failed, missing Captive or Captor data.'
        captive_sim_name = CommonSimNameUtils.get_full_name(captive_sim_info)
        captive_sim_id = CommonSimUtils.get_sim_id(captive_sim_info)
        captor_sim_name = CommonSimNameUtils.get_full_name(captor_sim_info)
        try:
            if not CommonRelationshipUtils.has_met(captor_sim_info, captive_sim_info) and not CommonRelationshipUtils.add_relationship_bit(captor_sim_info, captive_sim_info, CommonRelationshipBitId.HAS_MET):
                self.log.error('Failed to add Has Met Relationship Bit.')
            if not CommonRelationshipUtils.add_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT):
                self.log.error('Failed to add Captor/Captive Relationship Bit.')
            if not CommonRelationshipUtils.add_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT):
                self.log.error('Failed to add Captor Relationship Bit.')
            if not CommonRelationshipUtils.add_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT):
                self.log.error('Failed to add Captive Relationship Bit.')
            self._buff_utils.remove_appropriateness_related_buffs(captive_sim_info)

            SSCommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.LEAVE)
            SSCommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.LEAVE_NOW_MUST_RUN)
            SSCommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.SINGLE_SIM_LEAVE)
            captive_sim_data = SSSimData(captive_sim_info)
            captor_sim_id = CommonSimUtils.get_sim_id(captor_sim_info)
            captive_sim_data.captor_sim_id = captor_sim_id
            captor_sim_data = SSSimData(captor_sim_info)
            if captive_sim_id not in captor_sim_data.captive_sim_ids:
                captor_sim_data.captive_sim_ids += (captive_sim_id, )
            captive_sim_data.captor_household_id = CommonHouseholdUtils.get_household_id(captor_sim_info)
            CommonTraitUtils.add_trait(captive_sim_info, SSTraitId.PREVENT_LEAVE)
            CommonTraitUtils.add_trait(captive_sim_info, SSAbductionTraitId.CAPTIVE)
            SSAllowanceUtils().set_allow_all(captive_sim_info)
            CommonSimInteractionUtils.cancel_all_queued_or_running_interactions(captive_sim_info, cancel_reason='Became a Captive')
        except Exception as ex:
            self.log.error('Problem occurred while creating Captive \'{}\' with Captor \'{}\'.'.format(captive_sim_name, captor_sim_name), exception=ex)
            return False, 'Failed, Exception Occurred.'
        return True, 'Success, \'{}\' is now a Slave.'.format(CommonSimNameUtils.get_full_name(captive_sim_info))

    def refresh_captive(self, captive_sim_info: SimInfo) -> bool:
        """refresh_captive(slave_sim_info)

        Refresh the state of a Captive Sim.

        :param captive_sim_info: The Sim to refresh the state of.
        :type captive_sim_info: SimInfo
        :return: True, if the Sim was refreshed successfully. False, if not.
        :rtype: bool
        """
        CommonTraitUtils.remove_trait(captive_sim_info, SSTraitId.PREVENT_LEAVE)
        CommonTraitUtils.add_trait(captive_sim_info, SSTraitId.PREVENT_LEAVE)
        CommonTraitUtils.remove_trait(captive_sim_info, SSAbductionTraitId.CAPTIVE)
        CommonTraitUtils.add_trait(captive_sim_info, SSAbductionTraitId.CAPTIVE)
        return True

    def release_captive(self, captive_sim_info: SimInfo, releasing_sim_info: SimInfo=None) -> bool:
        """release_captive(captive_sim_info, releasing_sim_info=None)

        Release a Captive Sim from Captivity.

        :param captive_sim_info: The Captive being released.
        :type captive_sim_info: SimInfo
        :param releasing_sim_info: The Sim that is releasing the Captive. Default is None.
        :type releasing_sim_info: SimInfo, optional
        :return: True, if the Captive was released successfully. False, if not.
        :rtype: bool
        """
        if captive_sim_info is None:
            self.log.debug('captive_sim_info was None.')
            return False
        captive_sim_name = CommonSimNameUtils.get_full_name(captive_sim_info)
        captive_sim_id = CommonSimUtils.get_sim_id(captive_sim_info)
        try:
            self.log.debug('Attempting to release Captive \'{}\'.'.format(captive_sim_name))
            captive_sim_data = SSSimData(captive_sim_info)
            captor_sim_info = self.get_captor(captive_sim_info, instanced_only=False)
            if captor_sim_info is not None:
                captor_sim_name = CommonSimNameUtils.get_full_name(captor_sim_info)
                captor_sim_data = SSSimData(captor_sim_info)
                if captive_sim_id in captor_sim_data.captive_sim_ids:
                    new_captive_list = list(captor_sim_data.captive_sim_ids)
                    new_captive_list.remove(captive_sim_id)
                    captor_sim_data.captive_sim_ids = tuple(new_captive_list)
                self.log.format_with_message('Attempting to remove relationship bits between Sims.', sim=captive_sim_info, target=captor_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT)
                self.log.debug('Done removing relationship bits between Captor \'{}\' and Captive \'{}\'.'.format(captor_sim_name, captive_sim_name))
                self.log.debug('Done removing Captor relationships.')

            captive_sim_data.captor_sim_id = -1
            self.log.debug('Attempting to remove traits.')
            CommonTraitUtils.remove_trait(captive_sim_info, SSAbductionTraitId.CAPTIVE)
            self.log.debug('Attempting to remove buffs.')
            CommonTraitUtils.remove_trait(captive_sim_info, SSTraitId.PREVENT_LEAVE)
            SSAllowanceUtils().set_disallow_all(captive_sim_info)
            captive_sim_data.captor_household_id = -1
            self.log.debug('Done removing buffs.')
            self.log.debug('Attempting to remove situations.')
            SSCommonSituationUtils.remove_sim_from_situation(captive_sim_info, SSAbductionSituationId.PLAYER_ABDUCTED_NPC)
            self.log.debug('Done removing Sim from situations.')
            if not CommonSimTypeUtils.is_player_sim(captive_sim_info):
                self.log.debug('Attempting to make Sim leave.')
                SSCommonSituationUtils.make_sim_leave(captive_sim_info)
                self.log.debug('Done making Sim leave.')
            self.log.debug('Done releasing Captive \'{}\'.'.format(captive_sim_name))
        except Exception as ex:
            self.log.error('Problem occurred while releasing Captive \'{}\'.'.format(captive_sim_name), exception=ex)
            return False
        return True

    def release_captives_of(self, captor_sim_info: SimInfo) -> bool:
        """release_captives_of(captor_sim_info)

        Release all Captives of the specified Captor Sim.

        :param captor_sim_info: The Captor to release the Captives of.
        :type captor_sim_info: SimInfo
        :return: True, if all Captives of the specified Captor Sim were released successfully. False, if not.
        :rtype: bool
        """
        if captor_sim_info is None:
            self.log.debug('captor_sim_info was None.')
            return False
        captor_sim_name = CommonSimNameUtils.get_full_name(captor_sim_info)
        self.log.debug('Releasing All Captives of \'{}\'.'.format(captor_sim_name))
        captive_sim_info_list = self.get_captives(captor_sim_info)
        for captive_sim_info in captive_sim_info_list:
            self.release_captive(captive_sim_info, releasing_sim_info=captor_sim_info)
        self.log.debug('Done releasing Captives of Captor \'{}\'.'.format(captor_sim_info))
        return True

    def has_invalid_captive_state(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim has an invalid captive state. """
        return self.has_captor(sim_info)\
               and (not CommonSimSituationUtils.has_situations(sim_info, (SSAbductionSituationId.PLAYER_ABDUCTED_NPC, ))
                    or not CommonTraitUtils.has_trait(sim_info, SSAbductionTraitId.CAPTIVE))\
               and not CommonSimInteractionUtils.has_interaction_running_or_queued(sim_info, SSAbductionInteractionId.ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME)


@sims4.commands.Command('ss.show_captives', command_type=sims4.commands.CommandType.Live)
def _ss_abduction_show_captives(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing captives of active Sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    sim_info_list = SSAbductionStateUtils().get_captives(active_sim_info, instanced_only=False)
    if not sim_info_list:
        output('No captives were found for the Active Sim.')
    else:
        for sim_info in sim_info_list:
            output('\'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    output('Done displaying captives.')


@sims4.commands.Command('ss.show_captor', command_type=sims4.commands.CommandType.Live)
def _ss_abduction_show_captor(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing captor of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    captor_sim_info = SSAbductionStateUtils().get_captor(active_sim_info, instanced_only=False)
    if not captor_sim_info:
        output('No captor was found for the Active Sim.')
    else:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(captor_sim_info)))
    output('Done displaying captor.')
