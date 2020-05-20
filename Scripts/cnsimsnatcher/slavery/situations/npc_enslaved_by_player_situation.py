"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from distributor.shared_messages import IconInfoData
from event_testing.test_events import TestEvent
from sims.household import Household
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4.tuning.instances import lock_instance_tunables
from sims4.tuning.tunable import TunableTuple, TunableMapping
from sims4.tuning.tunable_base import GroupNames
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from situations.complex.service_npc_situation import TunableFinishJobStateAndTest
from situations.service_npcs import ServiceNpcEndWorkReason
from situations.service_npcs.butler.butler_loot_ops import ButlerSituationStates
from situations.situation import Situation
from situations.situation_complex import CommonSituationState
import event_testing
import services
from typing import Tuple, Any

from role.role_state import RoleState
from situations.situation_complex import SituationState, SituationStateData
from situations.situation_job import SituationJob
from situations.visiting.visiting_situation_common import VisitingNPCSituation
import sims4.tuning.tunable
import tunable_time
from situations.situation_types import SituationCreationUIOption
from situations.bouncer.bouncer_types import BouncerExclusivityCategory


class SSSlaveSituationStateMixin(CommonSituationState):
    """ A base class for slave situation states. """

    def on_activate(self, reader=None) -> Any:
        """ What happens when the state is activated. """
        super().on_activate(reader)
        finish_job_states = self.owner.finish_job_states
        for (_, finish_job_state) in finish_job_states.items():
            for (_, custom_key) in finish_job_state.enter_state_test.get_custom_event_registration_keys():
                self._test_event_register(event_testing.test_events.TestEvent.InteractionComplete, custom_key)

    def handle_event(self, sim_info: SimInfo, event: Any, resolver: Any) -> Any:
        """ What happens when an event occurs. """
        finish_job_states = self.owner.finish_job_states
        for (finish_reason, finish_job_state) in finish_job_states.items():
            if resolver(finish_job_state.enter_state_test):
                self._change_state(SSLeaveSituationState(finish_reason))
                break

    def _test_event(self, event: Any, sim_info: SimInfo, resolver, test) -> Any:
        if event in test.test_events:
            return self.owner.test_interaction_complete_by_job_holder(sim_info, resolver, self.owner.default_job(), test)
        return False

    def timer_expired(self) -> Any:
        """ What happens when the timer expires. """
        self.owner.try_set_next_state(self.next_state())

    @property
    def next_state(self) -> Any:
        """ The next state to perform. """
        raise NotImplementedError()

    @property
    def situation_state(self) -> ButlerSituationStates:
        """The situation state identifier. """
        raise NotImplementedError()


class _SSSlaveCleaningState(SSSlaveSituationStateMixin):

    # noinspection PyMissingOrEmptyDocstring
    @property
    def next_state(self) -> Any:
        return self.owner.slave_job_states.gardening_state

    # noinspection PyMissingOrEmptyDocstring
    @property
    def situation_state(self) -> ButlerSituationStates:
        return ButlerSituationStates.CLEANING


class _SSSlaveGardeningState(SSSlaveSituationStateMixin):

    # noinspection PyMissingOrEmptyDocstring
    @property
    def next_state(self) -> Any:
        return self.owner.slave_job_states.repair_state

    # noinspection PyMissingOrEmptyDocstring
    @property
    def situation_state(self) -> ButlerSituationStates:
        return ButlerSituationStates.GARDENING


class _SSSlaveChildcareState(SSSlaveSituationStateMixin):

    # noinspection PyMissingOrEmptyDocstring
    @property
    def next_state(self) -> Any:
        return self.owner.slave_job_states.default_state

    # noinspection PyMissingOrEmptyDocstring
    @property
    def situation_state(self) -> ButlerSituationStates:
        return ButlerSituationStates.CHILDCARE


class _SSSlaveRepairState(SSSlaveSituationStateMixin):

    # noinspection PyMissingOrEmptyDocstring
    @property
    def next_state(self) -> Any:
        return self.owner.slave_job_states.childcare_state

    # noinspection PyMissingOrEmptyDocstring
    @property
    def situation_state(self) -> ButlerSituationStates:
        return ButlerSituationStates.REPAIR


class _SSSlaveDefaultState(SSSlaveSituationStateMixin):

    # noinspection PyMissingOrEmptyDocstring
    @property
    def next_state(self) -> Any:
        return self.owner.slave_job_states.cleaning_state

    # noinspection PyMissingOrEmptyDocstring
    @property
    def situation_state(self) -> ButlerSituationStates:
        return ButlerSituationStates.DEFAULT


class SSLeaveSituationState(SituationState):
    """ A state that handles a Sim leaving. """

    def __init__(self, leave_role_reason: str=None):
        super().__init__()
        self._leave_role_reason = leave_role_reason

    def on_activate(self, reader=None) -> None:
        super().on_activate(reader)
        if reader is not None:
            return
        slave_sim = self.owner.slave_sim()
        self.owner._on_leaving_situation(self._leave_role_reason)
        if slave_sim is None:
            return
        services.get_zone_situation_manager().make_sim_leave_now_must_run(slave_sim)


class SSSlaveryNPCEnslavedByPlayerSituation(VisitingNPCSituation):
    """ The situation used when the player enslaves an NPC. """
    INSTANCE_TUNABLES = {
        'slave_sim_job': sims4.tuning.tunable.TunableTuple(
            situation_job=SituationJob.TunableReference(
                description='\n                          The situation job for the sim that was enslaved.\n                          '
            ),
            staying_role_state=RoleState.TunableReference(
                description='\n                          The role state for the sim that was enslaved.\n                          '
            )
        ),
        'slave_job_states': TunableTuple(
            cleaning_state=_SSSlaveCleaningState.TunableFactory(
                description='\n                Situation State for the slave to run all the clean \n                interactions.\n                '
            ),
            gardening_state=_SSSlaveGardeningState.TunableFactory(
                description='\n                Situation State for the slave to run all the gardening\n                interactions.\n                '
            ),
            childcare_state=_SSSlaveChildcareState.TunableFactory(
                description='\n                Situation State for the slave to run all the childcare\n                interactions.\n                '
            ),
            repair_state=_SSSlaveRepairState.TunableFactory(
                description='\n                Situation State for the slave to run all the repair\n                interactions.\n                '
            ),
            default_state=_SSSlaveDefaultState.TunableFactory(
                description='\n                Situation State for the slave to run all its default\n                interaction when no other service state is selected.\n                '
            ),
            tuning_group=GroupNames.SITUATION
        ),
        'when_to_refresh_situation': tunable_time.TunableTimeSpan(
            description='\n            The amount of time that needs to pass before refreshing the situation.\n            ',
            default_hours=7
        ),
        'finish_job_states': TunableMapping(
            description='\n            Tune pairs of job finish role states with job finish tests. When\n            those tests pass, the sim will transition to the paired role state.\n            The situation will also be transitioned to the Leaving situation\n            state.\n            ',
            key_type=ServiceNpcEndWorkReason,
            value_type=TunableFinishJobStateAndTest()
        )
    }
    REMOVE_INSTANCE_TUNABLES = Situation.NON_USER_FACING_REMOVE_INSTANCE_TUNABLES

    __slots__ = {'slave_sim_job', 'slave_job_states', 'finish_job_states', 'when_to_refresh_situation'}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._locked_states = set()
        self._owning_household: Household = CommonHouseholdUtils.get_active_household()
        self._service_start_time = services.time_service().sim_now

    @classmethod
    def _states(cls) -> Tuple[SituationStateData]:
        result: Tuple[SituationStateData] = (
            SituationStateData(1, _SSSlaveDefaultState, factory=cls.slave_job_states.default_state),
            SituationStateData(2, _SSSlaveCleaningState, factory=cls.slave_job_states.default_state),
            SituationStateData(3, _SSSlaveGardeningState, factory=cls.slave_job_states.default_state),
            SituationStateData(4, _SSSlaveChildcareState, factory=cls.slave_job_states.default_state),
            SituationStateData(5, _SSSlaveRepairState, factory=cls.slave_job_states.default_state),
            SituationStateData(6, SSLeaveSituationState, factory=cls.slave_job_states.default_state)
        )
        return result

    @classmethod
    def _get_tuned_job_and_default_role_state_tuples(cls) -> Any:
        return list(cls.slave_job_states.default_state._tuned_values.job_and_role_changes.items())

    @classmethod
    def default_job(cls) -> SituationJob:
        """ This is the default job that Sims will be put into. """
        return cls.slave_sim_job.situation_job

    def start_situation(self) -> None:
        """ Start the situation. """
        super().start_situation()
        self._change_state(self.slave_job_states.default_state())

    def _destroy(self) -> None:
        super()._destroy()

    def _get_duration(self) -> int:
        super()._get_duration()
        if self._seed.duration_override is not None:
            return self._seed.duration_override
        return self.when_to_refresh_situation().in_minutes()

    def try_set_next_state(self, new_situation_state) -> Any:
        """ Try to set the next state. """
        if new_situation_state.situation_state in self._locked_states:
            new_situation_state.owner = self
            self.try_set_next_state(new_situation_state.next_state())
            return
        self._change_state(new_situation_state)

    def slave_sim(self) -> Sim:
        """ The slave Sim. """
        sim = next(self.all_sims_in_situation_gen(), None)
        return sim

    def enable_situation_state(self, new_situation_state) -> None:
        """ Enables a state. """
        if new_situation_state in self._locked_states:
            self._locked_states.remove(new_situation_state)
        services.get_event_manager().process_event(TestEvent.AvailableDaycareSimsChanged, sim_info=self.slave_sim().sim_info)

    def disable_situation_state(self, new_situation_state) -> None:
        """ Disables a state. """
        self._locked_states.add(new_situation_state)
        if self._cur_state.situation_state == new_situation_state:
            self.try_set_next_state(self._cur_state)
        services.get_event_manager().process_event(TestEvent.AvailableDaycareSimsChanged, sim_info=self.slave_sim().sim_info)

    @property
    def is_in_childcare_state(self) -> bool:
        """ Determine if the situation is currently in the child care state. """
        return ButlerSituationStates.CHILDCARE not in self._locked_states

    def _save_custom_situation(self, writer) -> None:
        super()._save_custom_situation(writer)
        writer.write_uint64('household_id', self._owning_household.id)

    def _on_set_sim_job(self, sim: Sim, job_type) -> None:
        # noinspection PyUnresolvedReferences
        self._owning_household.object_preference_tracker.update_preference_if_possible(sim.sim_info)
        services.get_event_manager().process_event(TestEvent.AvailableDaycareSimsChanged, sim_info=self.slave_sim().sim_info)

    def _on_leaving_situation(self, end_work_reason: str) -> str:
        return end_work_reason

    def _send_leave_notification(self, end_work_reason, *localization_args) -> None:
        end_work_tuning = self.finish_job_states[end_work_reason]
        notification = end_work_tuning.notification
        if notification is None:
            return
        for client in services.client_manager().values():
            recipient = client.active_sim
            if recipient is not None:
                dialog = notification(recipient)
                dialog.show_dialog(additional_tokens=localization_args, icon_override=IconInfoData(obj_instance=self.slave_sim()))
                break


sims4.tuning.instances.lock_instance_tunables(
    SSSlaveryNPCEnslavedByPlayerSituation,
    exclusivity=BouncerExclusivityCategory.VISIT,
    suppress_scoring_progress_bar=True,
    disallows_curfew_violation=False,
    creation_ui_option=SituationCreationUIOption.NOT_AVAILABLE,
    duration=0,
    _implies_greeted_status=True,
    venue_situation_player_job=None
)