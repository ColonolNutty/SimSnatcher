"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Any, Set

from cnsimsnatcher.abduction.utils.abduction_state_utils import SSAbductionStateUtils
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.persistence.ss_sim_data_storage import SSSimDataStore
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from objects.components.buff_component import BuffComponent
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 'ss_allowance_injection')


class _SSVanillaBuffComponent:
    @staticmethod
    def _is_appropriate(original_self: BuffComponent, tags: Set[Any]) -> bool:
        owning_sim_info = CommonSimUtils.get_sim_info(original_self.owner)
        if owning_sim_info is None:
            return True
        if not SSAbductionStateUtils().has_captors(owning_sim_info, instanced_only=False) and not SSSlaveryStateUtils().has_masters(owning_sim_info, instanced_only=False):
            return True
        log.debug('Checking if \'{}\' is allowed.'.format(CommonSimNameUtils.get_full_name(owning_sim_info)))
        sim_data = SSSimDataStore(owning_sim_info)
        if not sim_data.allowances & tags:
            log.debug('Not allowed. Allowance Tags: \'{}\' Tags: \'{}\''.format(pformat(sim_data.allowances), pformat(tags)))
            return False
        log.debug('Allowed. Allowance Tags: \'{}\' Tags: \'{}\''.format(pformat(sim_data.allowances), pformat(tags)))
        return True


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), BuffComponent, BuffComponent.is_appropriate.__name__)
def _ss_allowances_get_appropriateness(original, self, tags: Any) -> bool:
    return _SSVanillaBuffComponent._is_appropriate(self, tags) and original(self, tags)
