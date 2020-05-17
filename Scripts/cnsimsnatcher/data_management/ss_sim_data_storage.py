from typing import Set

from cnsimsnatcher.modinfo import ModInfo
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.common_sim_data_storage import CommonSimDataStorage


class SSSimDataStorage(CommonSimDataStorage):
    """ Data storage for SS. """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_sim_data_storage'

    @property
    def allowances(self) -> Set[CommonGameTag]:
        """ Retrieve the allowances for the Sim. """
        return self.get_data(default={
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
        })

    @allowances.setter
    def allowances(self, value: Set[CommonGameTag]):
        self.set_data(value)
