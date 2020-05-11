"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from cnsimsnatcher.abduction.enums.skill_ids import SSAbductionSkillId
from cnsimsnatcher.abduction.settings.setting_utils import SSAbductionSettingUtils
from interactions import ParticipantType
from cnsimsnatcher.abduction.enums.statistic_ids import SSAbductionStatisticId
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.operations.abduction_score import SSAbductionSuccessChanceOperation
from event_testing.test_based_score import TestBasedScore
from sims.sim_info import SimInfo
from sims4.sim_irq_service import yield_to_irq
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'ss_attempt_to_abduct_score')


class SSAbductionAttemptToAbductTestBasedScore(TestBasedScore):
    """ Calculate the chance of a successful abduction. """
    @classmethod
    def _verify_tuning_callback(cls) -> None:
        pass

    @classmethod
    def _tuning_loaded_callback(cls) -> None:
        pass

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=0)
    def get_score(cls, resolver) -> int:
        yield_to_irq()
        if resolver is not None:
            log.format(
                resolver_type=type(resolver),
                resolver_class=resolver.__class__,
                resolver_class_name=resolver.__class__.__name__
            )
        log.debug('Determining if abduction is successful.')
        sim = resolver.get_participant(ParticipantType.Actor)
        target = resolver.get_participant(ParticipantType.TargetSim) or resolver.get_participant(ParticipantType.Listeners)
        if sim is None or target is None:
            log.debug('Failed, Abduction Attempt is missing either the sim or the target, where did they go?')
            return 0
        sim_info = CommonSimUtils.get_sim_info(sim)
        target_sim_info = CommonSimUtils.get_sim_info(target)
        result = cls._get_result(sim_info, target_sim_info)
        CommonSimStatisticUtils.set_statistic_value(sim_info, SSAbductionStatisticId.ABDUCTION_WAS_SUCCESS, result)
        return result

    @classmethod
    def _get_result(cls, sim_info: SimInfo, target_sim_info: SimInfo) -> int:
        if SSAbductionSettingUtils().cheats.always_successful():
            log.debug('Guaranteed Abduction Attempt. Always successful setting is enabled.')
            return 1
        if CommonSimSkillUtils.is_at_max_skill_level(sim_info, SSAbductionSkillId.ABDUCTION):
            log.debug('Success, Active Sim is max level Domination.')
            return 1
        if SSAbductionSuccessChanceOperation.abduction_is_successful(sim_info):
            log.debug('Success, Abduction attempt was previously successful.')
            return 1
        if SSAbductionSuccessChanceOperation.abduction_is_failure(sim_info):
            log.debug('Failure, Abduction attempt was previously a failure.')
            return 0
        success_chance = SSAbductionSuccessChanceOperation.calculate_success_chance(sim_info, target_sim_info)
        if success_chance >= SSAbductionSuccessChanceOperation.ABDUCTION_SUCCESS_THRESHOLD:
            log.debug('Success, Abduction attempt is successful.')
            return 1
        log.debug('Failed, Abduction attempt has failed.')
        return 0

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def passes_threshold(cls, resolver, threshold) -> bool:
        if resolver is not None:
            log.format(
                resolver_type=type(resolver),
                resolver_class=resolver.__class__,
                resolver_class_name=resolver.__class__.__name__
            )
        if threshold is not None:
            log.format(
                threshold_type=type(threshold),
                threshold_class=threshold.__class__
            )
        return threshold.compare(cls.get_score(resolver))
