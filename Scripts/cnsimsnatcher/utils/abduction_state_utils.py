"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
import sims4.commands
from cnsimsnatcher.enums.buff_identifiers import SSBuffId
from cnsimsnatcher.enums.relationship_bit_identifiers import SSRelationshipBitId
from cnsimsnatcher.enums.situation_identifiers import SSSituationId
from cnsimsnatcher.enums.string_identifiers import SSStringId
from cnsimsnatcher.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from ssutilities.commonlib.utils.common_situation_utils import CommonSituationUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_abduction_state_utils')


class SSAbductionStateUtils:
    """ Utilities for abduction state. """
    @staticmethod
    def has_abducted_sims(sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a sim has abducted any sims. """
        return CommonRelationshipUtils.has_relationship_bit_with_any_sims(sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_HAS_CAPTURED_SIM_REL_BIT, instanced_only=instanced_only)

    @staticmethod
    def has_been_abducted(sim_info: SimInfo, instanced_only: bool=True) -> bool:
        """ Determine if a sim has been abducted. """
        return CommonBuffUtils.has_buff(sim_info, SSBuffId.SS_ABDUCTION_WAS_ABDUCTED_INVISIBLE)\
               or CommonRelationshipUtils.has_relationship_bit_with_any_sims(sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_IS_CAPTURED_BY_SIM_REL_BIT, instanced_only=instanced_only)

    @staticmethod
    def is_hostage_of(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """ Determine if a sim is the hostage of the specified sim. """
        return CommonRelationshipUtils.has_relationship_bit_with_sim(
            sim_info,
            target_sim_info,
            SSRelationshipBitId.SS_ABDUCTION_CAPTOR_SIM_TO_HOSTAGE_SIM_REL_BIT
        )\
               and CommonRelationshipUtils.has_relationship_bit_with_sim(
            sim_info,
            target_sim_info,
            SSRelationshipBitId.SS_ABDUCTION_SIM_IS_CAPTURED_BY_SIM_REL_BIT
        )

    @staticmethod
    def get_sims_with_captor_hostage_relationships_with(sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve the SimInfo of all Sims with a Captor/Hostage relationship with the specified sim. """
        return tuple(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(sim_info, SSRelationshipBitId.SS_ABDUCTION_CAPTOR_SIM_TO_HOSTAGE_SIM_REL_BIT, instanced_only=instanced_only))

    @staticmethod
    def get_hostages(captor_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve the SimInfo of all hostages the specified sim has captive. """
        return tuple(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(captor_sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_HAS_CAPTURED_SIM_REL_BIT, instanced_only=instanced_only))

    @staticmethod
    def get_captors(hostage_sim_info: SimInfo, instanced_only: bool=True) -> Tuple[SimInfo]:
        """ Retrieve the SimInfo of all captors that are holding the specified sim hostage. """
        return tuple(CommonRelationshipUtils.get_sim_info_of_all_sims_with_relationship_bit_generator(hostage_sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_IS_CAPTURED_BY_SIM_REL_BIT, instanced_only=instanced_only))

    @staticmethod
    def add_abduction_data(captor_sim_info: SimInfo, captive_sim_info: SimInfo):
        """ Add abduction data between two sims. """
        if not CommonRelationshipUtils.has_met(captor_sim_info, captive_sim_info) and not CommonRelationshipUtils.add_relationship_bit(captor_sim_info, captive_sim_info, CommonRelationshipBitId.HAS_MET):
            log.error('Failed to add Has Met Relationship Bit.')
        if not CommonRelationshipUtils.add_relationship_bit(captor_sim_info, captive_sim_info, SSRelationshipBitId.SS_ABDUCTION_CAPTOR_SIM_TO_HOSTAGE_SIM_REL_BIT):
            log.error('Failed to add Abduction Relationship Bit.')
        if not CommonRelationshipUtils.add_relationship_bit(captive_sim_info, captor_sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_IS_CAPTURED_BY_SIM_REL_BIT):
            log.error('Failed to add Captor Relationship Bit.')
        if not CommonRelationshipUtils.add_relationship_bit(captor_sim_info, captive_sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_HAS_CAPTURED_SIM_REL_BIT):
            log.error('Failed to add Hostage Relationship Bit.')
        CommonBuffUtils.add_buff(captive_sim_info, SSBuffId.SS_ABDUCTION_WAS_ABDUCTED_INVISIBLE, buff_reason=CommonLocalizationUtils.create_localized_string(SSStringId.ABDUCTION))
        CommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.LEAVE)
        CommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.LEAVE_NOW_MUST_RUN)
        CommonSituationUtils.remove_sim_from_situation(captive_sim_info, CommonSituationId.SINGLE_SIM_LEAVE)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def clear_abduction_data(to_clear_sim_info: SimInfo) -> bool:
        """ Clear abduction data from a sim. """
        if to_clear_sim_info is None:
            log.debug('sim_info was None.')
            return False
        log.format_with_message('Attempting to clear abduction data from sim.', sim=to_clear_sim_info)
        sim_info_list = SSAbductionStateUtils.get_sims_with_captor_hostage_relationships_with(to_clear_sim_info)
        if sim_info_list:
            for sim_info in sim_info_list:
                    log.format_with_message('Attempting to remove relationship bits between sims.', sim=to_clear_sim_info, target=sim_info)
                    CommonRelationshipUtils.remove_relationship_bit(to_clear_sim_info, sim_info, SSRelationshipBitId.SS_ABDUCTION_CAPTOR_SIM_TO_HOSTAGE_SIM_REL_BIT)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, to_clear_sim_info, SSRelationshipBitId.SS_ABDUCTION_CAPTOR_SIM_TO_HOSTAGE_SIM_REL_BIT)
                    CommonRelationshipUtils.remove_relationship_bit(to_clear_sim_info, sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_HAS_CAPTURED_SIM_REL_BIT)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, to_clear_sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_HAS_CAPTURED_SIM_REL_BIT)
                    CommonRelationshipUtils.remove_relationship_bit(sim_info, to_clear_sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_IS_CAPTURED_BY_SIM_REL_BIT)
                    CommonRelationshipUtils.remove_relationship_bit(to_clear_sim_info, sim_info, SSRelationshipBitId.SS_ABDUCTION_SIM_IS_CAPTURED_BY_SIM_REL_BIT)
                    log.debug('Done removing relationship bits.')
        else:
            log.debug('No captors found.')
        log.debug('Attempting to remove abduction buff.')
        CommonBuffUtils.remove_buff(to_clear_sim_info, SSBuffId.SS_ABDUCTION_WAS_ABDUCTED_INVISIBLE)
        log.debug('Done removing abduction buff.')
        log.debug('Attempting to remove abduction situation.')
        CommonSituationUtils.remove_sim_from_situation(to_clear_sim_info, SSSituationId.SS_ABDUCTION_PLAYER_ABDUCTED_NPC)
        log.debug('Done removing sim from abduction situation.')
        log.debug('Making sim leave.')
        CommonSituationUtils.make_sim_leave(to_clear_sim_info)
        log.debug('Done making sim leave.')
        return True

    @staticmethod
    def has_invalid_abduction_state(sim_info: SimInfo) -> bool:
        """ Determine if a Sim has an invalid abduction state. """
        from cnsimsnatcher.enums.interaction_identifiers import SSInteractionId
        return SSAbductionStateUtils.has_been_abducted(sim_info)\
               and not CommonSituationUtils.has_situation(sim_info, SSSituationId.SS_ABDUCTION_PLAYER_ABDUCTED_NPC)\
               and not CommonSimInteractionUtils.has_interaction_running_or_queued(sim_info, SSInteractionId.SS_ABDUCTION_ATTEMPT_TO_ABDUCT_HUMAN_SUCCESS_OUTCOME)


@sims4.commands.Command('simsnatcher.show_hostages', command_type=sims4.commands.CommandType.Live)
def _ss_abduction_show_hostage_names(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing hostages of active sim')
    active_sim_info = CommonSimUtils.get_active_sim_info()
    hostage_sim_info_list = SSAbductionStateUtils.get_hostages(active_sim_info)
    for hostage_sim_info in hostage_sim_info_list:
        output('\'{}\''.format(CommonSimNameUtils.get_full_name(hostage_sim_info)))
    output('Done displaying hostages.')
