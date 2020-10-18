"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from cnsimsnatcher.slavery.utils.slavery_state_utils import SSSlaveryStateUtils
from distributor.shared_messages import IconInfoData
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class SSSlaveryAttemptToEnslaveSuccessInteraction(CommonImmediateSuperInteraction):
    """ Handles the success outcome of an attempt to enslave. """

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
        self.log.debug('Attempt To Enslave was Successful!')
        # The one to be Master.
        master_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        # The one to be Slave.
        slave_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        SSSlaveryStateUtils().create_slave(slave_sim_info, master_sim_info)
        CommonBasicNotification(
            SSSlaveryStringId.SLAVERY,
            SSSlaveryStringId.SIM_HAS_ENSLAVED_SIM,
            description_tokens=(master_sim_info, slave_sim_info)
        ).show(
            icon=IconInfoData(obj_instance=master_sim_info),
            secondary_icon=IconInfoData(obj_instance=slave_sim_info)
        )
        self.log.debug('Finished succeeding enslave.')
        return True


class SSSlaveryAttemptToEnslaveFailureInteraction(CommonImmediateSuperInteraction):
    """ Handles the failure outcome of an attempt to enslave. """

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
        self.log.debug('Attempt To Enslave Failed!')
        # The one to be Master.
        master_sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        # The one to be Slave.
        slave_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        CommonBasicNotification(
            SSSlaveryStringId.SLAVERY,
            SSSlaveryStringId.SIM_FAILED_TO_ENSLAVE_SIM,
            description_tokens=(master_sim_info, slave_sim_info)
        ).show(
            icon=IconInfoData(obj_instance=master_sim_info),
            secondary_icon=IconInfoData(obj_instance=slave_sim_info)
        )
        self.log.debug('Finished failing enslave.')
        return True
