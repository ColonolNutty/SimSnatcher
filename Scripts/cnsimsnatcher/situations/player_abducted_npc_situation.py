"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, List

from role.role_state import RoleState
from situations.situation_complex import SituationState, SituationStateData
from situations.situation_job import SituationJob
from situations.visiting.visiting_situation_common import VisitingNPCSituation
import sims4.tuning.instances
import sims4.tuning.tunable
import tunable_time
from situations.situation_types import SituationCreationUIOption
from situations.bouncer.bouncer_types import BouncerExclusivityCategory


class SSAbductionPlayerAbductedNPCSituation(VisitingNPCSituation):
    """ The situation used when the player abducts an NPC. """
    INSTANCE_TUNABLES = {
        'hostage_sim_job': sims4.tuning.tunable.TunableTuple(
            situation_job=SituationJob.TunableReference(
                description='\n                          The situation job for the sim that was abducted.\n                          '
            ),
            staying_role_state=RoleState.TunableReference(
                description='\n                          The role state for the sim that was abducted.\n                          '
            )
        ),
        'when_to_refresh_situation': tunable_time.TunableTimeSpan(
            description='\n            The amount of time that needs to pass before refreshing the situation.\n            ',
            default_hours=7
        )
    }

    __slots__ = {'hostage_sim_job', 'when_to_refresh_situation'}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def _states(cls) -> Tuple[SituationStateData]:
        return SituationStateData(1, _StayState),

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls) -> List[Tuple[SituationJob, RoleState]]:
        return [(cls.hostage_sim_job.situation_job, cls.hostage_sim_job.staying_role_state)]

    @classmethod
    def default_job(cls) -> SituationJob:
        """ This is the default job that Sims will be put into. """
        return cls.hostage_sim_job.situation_job

    def start_situation(self) -> None:
        """ Start the situation. """
        super().start_situation()
        self._change_state(_StayState())

    def _destroy(self) -> None:
        super()._destroy()

    def _get_duration(self) -> int:
        super()._get_duration()
        if self._seed.duration_override is not None:
            return self._seed.duration_override
        return self.when_to_refresh_situation().in_minutes()


sims4.tuning.instances.lock_instance_tunables(
    SSAbductionPlayerAbductedNPCSituation,
    exclusivity=BouncerExclusivityCategory.VISIT,
    suppress_scoring_progress_bar=True,
    disallows_curfew_violation=False,
    creation_ui_option=SituationCreationUIOption.NOT_AVAILABLE,
    duration=0,
    _implies_greeted_status=True
)


class _StayState(SituationState):
    pass

