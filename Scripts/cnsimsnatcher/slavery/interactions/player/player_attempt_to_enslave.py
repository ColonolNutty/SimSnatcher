"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from cnsimsnatcher.modinfo import ModInfo
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_social_mixer_interaction import CommonSocialMixerInteraction


class SSSlaveryAttemptToEnslaveInteraction(CommonSocialMixerInteraction):
    """ Handles the success outcome of an attempt to abduct. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_start_slavery'

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        self.log.debug('Attempting to Enslave a Sim')
        return super().on_started(interaction_sim, interaction_target)
