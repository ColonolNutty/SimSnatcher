"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Tuple

from cnsimsnatcher.enums.interaction_ids import SSInteractionId
from cnsimsnatcher.modinfo import ModInfo
from objects.script_object import ScriptObject
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _SSDebugSimInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            SSInteractionId.SS_DEBUG_SUMMON_CAPTIVES_AND_SLAVES,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        return CommonTypeUtils.is_sim_or_sim_info(script_object)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'thingy')
log.enable()


@sims4.commands.Command('ss.do_it', command_type=sims4.commands.CommandType.Live)
def _ss_do_it(_connection: int=None):
    try:
        log.debug('Doing it.')
        output = sims4.commands.CheatOutput(_connection)
        output('Doing it.')
        sim = CommonSimUtils.get_active_sim()
        log.format(sim=sim)

        def _log_thingy(thing, name: str):
            if thing is not None:
                log.format_with_message(name, posture=thing, posture_type=type(thing), posture_class=thing.__class__, dir_val=dir(thing))
            else:
                log.debug('No {}'.format(name))

        try:
            posture = sim.posture
            _log_thingy(posture, 'posture')
        except Exception as ex:
            log.error('Failed posture', exception=ex)

        try:
            target_posture = sim.target_posture
            _log_thingy(target_posture, 'target_posture')
        except Exception as ex:
            log.error('Failed target_posture', exception=ex)

        try:
            # noinspection PyPropertyAccess
            posture_state = sim.posture_state
            _log_thingy(posture_state, 'posture_state')
        except Exception as ex:
            log.error('Failed posture state.', exception=ex)

        try:
            posture_target = sim.posture_target
            _log_thingy(posture_target, 'posture_target')
        except Exception as ex:
            log.error('Failed posture_target', exception=ex)

        output('Done')
    except Exception as ex:
        log.error('Failed for some reason', exception=ex)
