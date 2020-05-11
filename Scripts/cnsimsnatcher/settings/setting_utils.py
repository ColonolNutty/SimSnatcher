"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.sims.common_age_species_utils import CommonAgeSpeciesUtils


class SSSettingUtils(CommonService):
    """ Utilities to get SS settings. """
    def __init__(self) -> None:
        super().__init__()
        from cnsimsnatcher.data_management.data_manager_utils import SSDataManagerUtils
        self._settings_manager = SSDataManagerUtils().get_global_mod_settings_manager()

    def is_enabled_for_interactions(self, sim_info: SimInfo) -> bool:
        """is_enabled_for_interactions(sim_info)

        Determine if a Sim is enabled to use the Sim Snatcher interactions.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is enabled for interactions. False, if not.
        :rtype: bool
        """
        return CommonAgeSpeciesUtils.is_teen_adult_or_elder_human(sim_info)
