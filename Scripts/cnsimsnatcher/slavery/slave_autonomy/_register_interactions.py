"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from cnsimsnatcher.slavery.enums.interaction_ids import SSSlaveryInteractionId
from objects.game_object import GameObject
from objects.script_object import ScriptObject
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_tag_utils import CommonObjectTagUtils


@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _SSSlaveryFridgeAutonomyInteractionHandler(CommonScriptObjectInteractionHandler):
    # noinspection PyMissingOrEmptyDocstring
    @property
    def interactions_to_add(self) -> Tuple[int]:
        result: Tuple[int] = (
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_GOURMET_AUTONOMOUSLY,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_GOURMET_AUTONOMOUSLY_VEGETARIAN,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_AUTONOMOUSLY,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_AUTONOMOUSLY_VEGETARIAN,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_FAMILY_MEAL_AUTONOMOUSLY,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_FAMILY_MEAL_AUTONOMOUSLY_VEGETARIAN,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_PARTY_MEAL_AUTONOMOUSLY,
            SSSlaveryInteractionId.SLAVE_FRIDGE_COOK_PARTY_MEAL_AUTONOMOUSLY_VEGETARIAN,
        )
        return result

    # noinspection PyMissingOrEmptyDocstring
    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        if not CommonTypeUtils.is_game_object(script_object):
            return False
        script_object: GameObject = script_object
        return CommonObjectTagUtils.has_game_tags(script_object, (CommonGameTag.FUNC_FRIDGE, ))
