"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List, Tuple, Union

import services
from sims.sim_info import SimInfo
from situations.dynamic_situation_goal_tracker import DynamicSituationGoalTracker
from situations.situation import Situation
from situations.situation_goal import SituationGoal
from situations.situation_goal_targeted_sim import SituationGoalTargetedSim
from situations.situation_goal_tracker import SituationGoalTracker
from tag import Tag
from whims.whim_set import WhimSetBaseMixin
from sims4communitylib.enums.situations_enum import CommonSituationId
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSituationUtils:
    """ Utilities for situations. """
    @staticmethod
    def has_leave_situation(sim_info: SimInfo) -> bool:
        """ Determine if a sim is currently involved in a leaving situation. """
        # noinspection PyUnresolvedReferences
        return CommonSituationUtils.has_situation(sim_info, CommonSituationId.LEAVE) or CommonSituationUtils.is_in_situations_with_any_tags(sim_info, (Tag.Role_Leave,))

    @staticmethod
    def make_sim_leave(sim_info: SimInfo):
        """ Make a sim leave the current lot. """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        services.get_zone_situation_manager().make_sim_leave(sim)

    @staticmethod
    def remove_sim_from_situation(sim_info: SimInfo, situation_id: int) -> bool:
        """ Remove a sim from the specified situation. """
        situation_manager = services.get_zone_situation_manager()
        if sim_info is None or situation_id is None:
            return False
        situation_manager.remove_sim_from_situation(sim_info, situation_id)
        return True

    @staticmethod
    def has_situation(sim_info: SimInfo, *situation_ids: int) -> bool:
        """ Determine if a sim is currently involved in a situation. """
        sim_situations = CommonSituationUtils.get_situations(sim_info)
        for situation in sim_situations:
            situation_id = getattr(situation, 'guid64', None)
            if situation_id in situation_ids:
                return True
        return False

    @staticmethod
    def has_situation_job(sim_info: SimInfo, situation_job_ids: Tuple[int]) -> bool:
        """ Determine if a sim is currently assigned any of the specified situation job. """
        sim_situations = CommonSituationUtils.get_situations(sim_info)
        for situation in sim_situations:
            for situation_job in situation.all_jobs_gen():
                situation_job_id = getattr(situation_job, 'guid64', None)
                if situation_job_id in situation_job_ids:
                    return True
        return False

    @staticmethod
    def is_in_situations_with_any_tags(sim_info: SimInfo, tags: Tuple[Tag]) -> bool:
        """ Determine if a Sim is currently in a situation with any of the specified tags. """
        tags = set(tags)
        situations = CommonSituationUtils.get_situations(sim_info)
        for tag in tags:
            for situation in situations:
                if tag in getattr(situation, 'tags', tuple()):
                    return True
                for situation_job in situation.all_jobs_gen():
                    if tag in getattr(situation_job, 'tags', tuple()):
                        return True
        return False

    @staticmethod
    def get_situations(sim_info: SimInfo) -> List[Situation]:
        """ Retrieve the current situations a sim is involved in. """
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        sim_instance = CommonSimUtils.get_sim_instance(sim_info)
        if sim_instance is None:
            return list()
        return services.get_zone_situation_manager().get_situations_sim_is_in(sim_instance)

    @staticmethod
    def create_visit_situation(sim_info: SimInfo):
        """ Create a visit situation for a Non-Player Sim."""
        sim = CommonSimUtils.get_sim_instance(sim_info)
        services.get_zone_situation_manager().create_visit_situation(sim)

    @staticmethod
    def get_situation_goals(sim_info: SimInfo) -> Tuple[Union[SituationGoal, SituationGoalTargetedSim]]:
        """ Retrieve the goals of all situations a Sim is currently in. """
        goal_instances: List[Union[SituationGoal, SituationGoalTargetedSim]] = list()
        for situation in CommonSituationUtils.get_situations(sim_info):
            goal_tracker = situation._get_goal_tracker()
            if goal_tracker is None:
                continue
            if isinstance(goal_tracker, SituationGoalTracker):
                if goal_tracker._realized_minor_goals is not None:
                    goal_instances.extend(goal_tracker._realized_minor_goals.keys())
                if goal_tracker._realized_main_goal is not None:
                    goal_instances.insert(0, goal_tracker._realized_main_goal)
            elif isinstance(goal_tracker, DynamicSituationGoalTracker):
                goal_instances.extend(goal_tracker.goals)
        return tuple(goal_instances)

    @staticmethod
    def complete_situation_goal(sim_info: SimInfo, situation_goal_id: int, target_sim_info: SimInfo=None):
        """ Complete a situation goal for the specified Sim."""
        from sims4communitylib.utils.sims.common_whim_utils import CommonWhimUtils
        goal_instances: List[Union[SituationGoal, SituationGoalTargetedSim, WhimSetBaseMixin]] = list()
        goal_instances.extend(CommonSituationUtils.get_situation_goals(sim_info))
        goal_instances.extend(CommonWhimUtils.get_current_whims(sim_info))
        for goal_instance in goal_instances:
            if goal_instance.guid64 != situation_goal_id:
                continue
            goal_instance.force_complete(target_sim=target_sim_info)
