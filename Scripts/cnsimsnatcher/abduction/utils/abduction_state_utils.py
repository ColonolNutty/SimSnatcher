"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
import sims4.commands
from cnsimsnatcher.abduction.enums.interaction_ids import SSAbductionInteractionId
from cnsimsnatcher.abduction.enums.relationship_bit_ids import SSAbductionRelationshipBitId
from cnsimsnatcher.abduction.enums.situation_ids import SSAbductionSituationId
from cnsimsnatcher.abduction.enums.string_ids import SSAbductionStringId
from cnsimsnatcher.abduction.enums.trait_ids import SSAbductionTraitId
from cnsimsnatcher.enums.buff_ids import SSBuffId
from cnsimsnatcher.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ssutilities.commonlib.utils.common_situation_utils import CommonSituationUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSAbductionStateUtils(HasLog):
    """ Utilities for managing Abduction state. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ssa_state_utils'

    def has_captives(self, captor_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has abducted any Sims. """
        return CommonRelationshipUtils.has_relationship_bit_with_any_sims(
            captor_sim_info,
            SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT,
            instanced_only=instanced_only
        )

    def has_captors(self, hostage_sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a Sim has been abducted. """
        return CommonTraitUtils.has_trait(hostage_sim_info, SSAbductionTraitId.CAPTIVE)\
               or CommonRelationshipUtils.has_relationship_bit_with_any_sims(
            hostage_sim_info,
            SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT,
            instanced_only=instanced_only
        )

    def is_captive_of(self, sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """ Determine if a Sim is the hostage of the specified Sim. """
        return CommonRelationshipUtils.has_relationship_bit_with_sim(
            sim_info,
            target_sim_info,
            SSAbductionRelationshipBitId.CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT
        )\
               and CommonRelationshipUtils.has_relationship_bit_with_sim(
            sim_info,
            target_sim_info,
            SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT
        )

    def get_captives(self, captor_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve a collection of Sims that are a Captive to the specified Sim. """
        return tuple(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(captor_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT, instanced_only=instanced_only))

    def get_captors(self, captive_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve a collection of Sims that are a Captor of the specified Sim. """
        return tuple(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(captive_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT, instanced_only=instanced_only))

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
            CommonBuffUtils.add_buff(captive_sim_info, SSBuffId.ALLOWED_NOTHING_INVISIBLE, buff_reason=CommonLocalizationUtils.create_localized_string(SSAbductionStringId.ABDUCTION))
            CommonBuffUtils.add_buff(captive_sim_info, SSBuffId.PREVENT_LEAVE_INVISIBLE, buff_reason=CommonLocalizationUtils.create_localized_string(SSAbductionStringId.ABDUCTION))
            CommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.LEAVE)
            CommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.LEAVE_NOW_MUST_RUN)
            CommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.SINGLE_SIM_LEAVE)
            CommonTraitUtils.add_trait(captive_sim_info, SSAbductionTraitId.CAPTIVE)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred while creating Captive \'{}\' with Captor \'{}\'.'.format(captive_sim_name, captor_sim_name), exception=ex)
            return False, 'Failed, Exception Occurred.'
        return True, 'Success, \'{}\' is now a Slave.'.format(CommonSimNameUtils.get_full_name(captive_sim_info))

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
        try:
            self.log.debug('Attempting to release Captive \'{}\'.'.format(captive_sim_name))
            if releasing_sim_info is not None and self.is_captive_of(captive_sim_info, releasing_sim_info):
                captor_sim_info_list = (releasing_sim_info,)
            else:
                captor_sim_info_list = self.get_captors(captive_sim_info)

            for captor_sim_info in captor_sim_info_list:
                self.log.format_with_message('Attempting to remove relationship bits between Sims.', sim=captive_sim_info, target=captor_sim_info)
                CommonRelationshipUtils.remove_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.CAPTOR_SIM_TO_CAPTIVE_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTOR_OF_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captor_sim_info, captive_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT)
                CommonRelationshipUtils.remove_relationship_bit(captive_sim_info, captor_sim_info, SSAbductionRelationshipBitId.SIM_IS_CAPTIVE_OF_SIM_REL_BIT)
                self.log.debug('Done removing relationship bits.')
            self.log.debug('Done removing Captor relationships.')

            self.log.debug('Attempting to remove traits.')
            CommonTraitUtils.remove_trait(captive_sim_info, SSAbductionTraitId.CAPTIVE)
            self.log.debug('Attempting to remove buffs.')
            CommonBuffUtils.remove_buff(captive_sim_info, SSBuffId.ALLOWED_NOTHING_INVISIBLE)
            CommonBuffUtils.remove_buff(captive_sim_info, SSBuffId.PREVENT_LEAVE_INVISIBLE)
            self.log.debug('Done removing buffs.')
            self.log.debug('Attempting to remove situations.')
            CommonSituationUtils.remove_sim_from_situation(captive_sim_info, SSAbductionSituationId.PLAYER_ABDUCTED_NPC)
            self.log.debug('Done removing Sim from situations.')
            self.log.debug('Attempting to make Sim leave.')
            CommonSituationUtils.make_sim_leave(captive_sim_info)
            self.log.debug('Done making Sim leave.')
            self.log.debug('Done releasing Captive \'{}\'.'.format(captive_sim_name))
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Problem occurred while releasing Captive \'{}\'.'.format(captive_sim_name), exception=ex)
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

    def has_invalid_abduction_state(self, sim_info: SimInfo) -> bool:
        """ Determine if a Sim has an invalid abduction state. """
        return self.has_captors(sim_info)\
               and (not CommonSituationUtils.has_situation(sim_info, SSAbductionSituationId.PLAYER_ABDUCTED_NPC)
                    or not CommonTraitUtils.has_trait(sim_info, SSAbductionTraitId.CAPTIVE))\
               and not CommonSimInteractionUtils.has_interaction_running_or_queued(sim_info, SSAbductionInteractionId.ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME)


@sims4.commands.Command('simsnatcher.show_hostages', command_type=sims4.commands.CommandType.Live)
def _ss_abduction_show_hostage_names(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing hostages of active Sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    sim_info_list = SSAbductionStateUtils().get_captives(active_sim_info)
    if not sim_info_list:
        output('No hostages were found for the Active Sim.')
    for sim_info in sim_info_list:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    output('Done displaying hostages.')


@sims4.commands.Command('simsnatcher.show_captors', command_type=sims4.commands.CommandType.Live)
def _ss_abduction__show_master_names(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing captors of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    sim_info_list = SSAbductionStateUtils().get_captors(active_sim_info)
    if not sim_info_list:
        output('No captors were found for the Active Sim.')
    for sim_info in sim_info_list:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(sim_info)))
    output('Done displaying captors.')
