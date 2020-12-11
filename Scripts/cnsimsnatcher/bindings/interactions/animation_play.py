"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union

from cnsimsnatcher.modinfo import ModInfo
from interactions.constraints import Constraint
from interactions.base.interaction import Interaction
from native.animation import NativeAsm
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_super_interaction import CommonConstrainedSuperInteraction, CommonBaseSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.resources.common_posture_constraint_service import CommonPostureConstraintService
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSAnimationPlayInteraction(CommonBaseSuperInteraction, CommonConstrainedSuperInteraction):
    """ An interaction used to play an animation. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_animation_play'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_constraint_gen(cls, inst: Interaction, sim: Sim, target: Any) -> Union[Constraint, None]:
        cls.get_log().format_with_message('Generating constraints.', inst=inst, sim=sim, target=target)
        return CommonPostureConstraintService().stand_or_swim_at_none

    # noinspection PyUnusedLocal
    def _setup_asm_default(self, interaction_sim: Sim, interaction_target: Sim, interaction_asm: NativeAsm, *args, **kwargs) -> Union[bool, None]:
        self.log.format_with_message('Setting up asm.', interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_asm=interaction_asm, argles=args, kwargles=kwargs)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        actor_param = 'a0'
        actor_animation_param = 'animation_name_a0'
        actor_animation_name = 'Hostage2:PosePack_201802180255249126_set_4'
        interaction_asm.set_parameter(actor_animation_param, actor_animation_name)
        interaction_asm.set_actor(actor_param, interaction_target)
        interaction_asm.enter()
        self.log.debug('Done setting up asm.')
        return True
