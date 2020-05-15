"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

from buffs import Appropriateness
from cnsimsnatcher.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils


class SSBuffUtils(HasLog):
    """ Utilities for managing buffs related to SS. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'ss_buff_utils'

    def remove_appropriateness_related_buffs(self, sim_info: SimInfo):
        """ Remove buffs related to appropriateness from a Sim. """
        appropriateness_buffs = {
            CommonGameTag.APPROPRIATENESS_BARTENDING,
            CommonGameTag.APPROPRIATENESS_BATHING,
            CommonGameTag.APPROPRIATENESS_CAKE,
            CommonGameTag.APPROPRIATENESS_CALL_TO_MEAL,
            CommonGameTag.APPROPRIATENESS_CLEANING,
            CommonGameTag.APPROPRIATENESS_COMPUTER,
            CommonGameTag.APPROPRIATENESS_COOKING,
            CommonGameTag.APPROPRIATENESS_DANCING,
            CommonGameTag.APPROPRIATENESS_EATING,
            CommonGameTag.APPROPRIATENESS_FRONT_DESK,
            CommonGameTag.APPROPRIATENESS_GRAB_SNACK,
            CommonGameTag.APPROPRIATENESS_GUEST,
            CommonGameTag.APPROPRIATENESS_HIRED_WORKER,
            CommonGameTag.APPROPRIATENESS_HOST,
            CommonGameTag.APPROPRIATENESS_NOT_DURING_WORK,
            CommonGameTag.APPROPRIATENESS_NOT_DURING_WORK_LUNCH,
            CommonGameTag.APPROPRIATENESS_PHONE,
            CommonGameTag.APPROPRIATENESS_PHONE_GAME,
            CommonGameTag.APPROPRIATENESS_PLAY_INSTRUMENT,
            CommonGameTag.APPROPRIATENESS_PLAYING,
            CommonGameTag.APPROPRIATENESS_READ_BOOKS,
            CommonGameTag.APPROPRIATENESS_SERVICE_NPC,
            CommonGameTag.APPROPRIATENESS_SHOWER,
            CommonGameTag.APPROPRIATENESS_SINGING,
            CommonGameTag.APPROPRIATENESS_SLEEPING,
            CommonGameTag.APPROPRIATENESS_SOCIAL_PICKER,
            CommonGameTag.APPROPRIATENESS_STEREO,
            CommonGameTag.APPROPRIATENESS_TV_WATCHING,
            CommonGameTag.APPROPRIATENESS_TIP,
            CommonGameTag.APPROPRIATENESS_TOUCHING,
            CommonGameTag.APPROPRIATENESS_TRASH,
            CommonGameTag.APPROPRIATENESS_VIEW,
            CommonGameTag.APPROPRIATENESS_VISITOR,
            CommonGameTag.APPROPRIATENESS_WORK_SCIENTIST,
            CommonGameTag.APPROPRIATENESS_WORKOUT
        }
        for buff in CommonBuffUtils.get_buffs(sim_info):
            appropriateness = buff.get_appropriateness(appropriateness_buffs)
            if appropriateness == Appropriateness.DONT_CARE:
                continue
            self.log.debug('Removing buff {}'.format(pformat(buff)))
            CommonBuffUtils.remove_buff(sim_info, CommonBuffUtils.get_buff_id(buff))
        self.log.debug('Done removing buffs related to appropriateness.')
