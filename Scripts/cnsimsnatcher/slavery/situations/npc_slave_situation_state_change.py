"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from enum import Int
except:
    # noinspection PyMissingOrEmptyDocstring
    class Int:
        pass
from typing import Any
from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from situations.situation import Situation
from sims4.tuning.tunable import TunablePackSafeReference, TunableVariant, TunableEnumEntry
import services
from interactions.utils.loot_basic_op import BaseLootOperation


class SSSlaveSituationState(Int):
    """ States a Slave may be in. """
    DEFAULT = 1
    CLEANING = 2
    GARDENING = 3
    CHILDCARE = 4
    REPAIR = 5


class SSSlaveSituationStateChange(BaseLootOperation, HasLog):
    """ Changes the state of a Slave situation. """

    # noinspection PyUnresolvedReferences
    FACTORY_TUNABLES = {
        'slave_situation': TunablePackSafeReference(
            description="\n            The Situation who's state will change.\n            ",
            manager=services.situation_manager()),
        'operation': TunableVariant(
            description='\n            Enable or disable operation for tuned tone.\n            ',
            locked_args={
                'enable': True,
                'disable': False
            },
            default='enable'
        ),
        'situation_state': TunableEnumEntry(
            description='\n            Situation state for the butler that should be enabled or disabled\n            depending on the operation.\n            ',
            tunable_type=SSSlaveSituationState,
            default=SSSlaveSituationState.DEFAULT,
            invalid_enums=(SSSlaveSituationState.DEFAULT,)
        )
    }

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'sss_change_situation_state'

    def __init__(self, *args, slave_situation: Situation, operation: bool, situation_state: SSSlaveSituationState, **kwargs):
        super().__init__(*args, **kwargs)
        HasLog.__init__(self)
        self._slave_situation = slave_situation
        self._operation = operation
        self._situation_state = situation_state

    def _apply_to_subject_and_target(self, subject: Any, target: Any, resolver):
        if subject is None:
            self.log.debug('No subject to change the state of.')
            return
        situation_manager = services.get_zone_situation_manager()
        slave_situation = situation_manager.get_situation_by_type(self._slave_situation)
        if slave_situation is None:
            self.log.error('Sim {} trying to switch situation state {} while not running the slave situation'.format(subject, self._situation_state))
            return
        self.log.debug('Changing the state of the Slave Situation to {}.'.format(self._situation_state))
        if self._operation:
            slave_situation.enable_situation_state(self._situation_state)
        else:
            slave_situation.disable_situation_state(self._situation_state)
