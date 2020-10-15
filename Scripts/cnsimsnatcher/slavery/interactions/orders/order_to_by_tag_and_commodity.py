import random
from typing import Any, Tuple, List

import services
from cnsimsnatcher.modinfo import ModInfo
from cnsimsnatcher.order_to.enums.string_ids import SSOrderToStringId
from cnsimsnatcher.settings.setting_utils import SSSettingUtils
from cnsimsnatcher.slavery.enums.string_ids import SSSlaveryStringId
from distributor.shared_messages import IconInfoData
from event_testing.results import TestResult
from interactions.base.interaction import Interaction
from interactions.context import InteractionContext
from objects.game_object import GameObject
from sims.sim import Sim
from sims4.resources import Types
from sims4.tuning.tunable import TunableList, TunableTuple, TunableReference, TunableEnumSet
from sims4.tuning.tunable_base import GroupNames
from sims4communitylib.classes.interactions.common_super_interaction import CommonSuperInteraction
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.objects.common_object_interaction_utils import CommonObjectInteractionUtils
from sims4communitylib.utils.objects.common_object_tag_utils import CommonObjectTagUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_state_utils import CommonSimStateUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from tag import Tag


class SSOrderToByTagAndCommodityInteraction(CommonSuperInteraction):
    """ Handles an interaction. """
    INSTANCE_TUNABLES = {
        'target_static_commodities': TunableList(
            description='\n            The list of static commodities to which this affordance will\n            advertise.\n            ',
            tunable=TunableTuple(
                description='\n                A single chunk of static commodity scoring data.\n                ',
                static_commodity=TunableReference(
                    description='\n                    The type of static commodity offered by this affordance.\n                    ',
                    manager=services.get_instance_manager(
                        Types.STATIC_COMMODITY
                    ),
                    pack_safe=True,
                    reload_dependent=True
                )
            ),
            tuning_group=GroupNames.AUTONOMY
        ),
        'exclude_target_static_commodities': TunableList(
            description='\n            The list of static commodities to which this affordance will\n            ignore.\n            ',
            tunable=TunableTuple(
                description='\n                A single chunk of static commodity scoring data.\n                ',
                static_commodity=TunableReference(
                    description='\n                    The type of static commodity offered by this affordance.\n                    ',
                    manager=services.get_instance_manager(
                        Types.STATIC_COMMODITY
                    ),
                    pack_safe=True,
                    reload_dependent=True
                )
            ),
            tuning_group=GroupNames.AUTONOMY
        ),
        'target_object_tags': TunableEnumSet(enum_type=Tag)
    }

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'ss_order_to_by_tag_and_commodity'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context)
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return TestResult.NONE
        sim_info = CommonSimUtils.get_sim_info(interaction_sim)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not SSSettingUtils().is_enabled_for_interactions(sim_info):
            cls.get_log().debug('Failed, Active Sim or Target Sim is not available for interactions.')
            return TestResult.NONE
        if CommonSimStateUtils.is_dying(sim_info):
            cls.get_log().debug('Failed, Active Sim is dying.')
            return cls.create_test_result(False, reason='Active Sim is dying.')
        if CommonSimStateUtils.is_dying(target_sim_info):
            cls.get_log().debug('Failed, Target Sim is dying.')
            return cls.create_test_result(False, reason='Target Sim is dying.')
        cls.get_log().debug('Success, can order.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline) -> bool:
        self.log.format_with_message('Running \'{}\' on_run.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        target_static_commodities = getattr(self, 'target_static_commodities', tuple())
        exclude_target_static_commodities = getattr(self, 'exclude_target_static_commodities', tuple())
        target_object_tags = getattr(self, 'target_object_tags', tuple())
        self.log.format(exclude_target_static_commodities=exclude_target_static_commodities, target_static_commodities=target_static_commodities, target_object_tags=target_object_tags)
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        objects_and_interactions = self._find_objects_and_interactions()
        self.log.format(objects_and_interactions=objects_and_interactions)
        if not objects_and_interactions:
            return False
        chosen_objects_and_interactions = random.choice(objects_and_interactions)
        target_object = chosen_objects_and_interactions[0]
        target_object_interactions = list(chosen_objects_and_interactions[1])
        random.shuffle(target_object_interactions)
        success = False
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        for target_interaction in target_object_interactions:
            enqueue_result = CommonSimInteractionUtils.queue_interaction(target_sim_info, CommonInteractionUtils.get_interaction_id(target_interaction), target=target_object)
            if enqueue_result:
                success = True
                break
            self.log.format(enqueue_result=enqueue_result, interaction_short_name=CommonInteractionUtils.get_interaction_short_name(target_interaction))
        if success:
            self.log.debug('Successfully located and queued an interaction.')
            CommonBasicNotification(
                SSOrderToStringId.ORDER_ACCEPTED,
                SSOrderToStringId.SIM_WILL_CARRY_OUT_ORDER,
                description_tokens=(target_sim_info, )
            ).show(icon=IconInfoData(obj_instance=target_sim_info))
        else:
            self.log.debug('Failed to locate an interaction.')
            CommonBasicNotification(
                SSSlaveryStringId.FAILED_TO_PERFORM,
                SSSlaveryStringId.SIM_FAILED_TO_LOCATE_APPROPRIATE_OBJECT_PLEASE_ENSURE,
                description_tokens=(target_sim_info, )
            ).show(icon=IconInfoData(obj_instance=target_sim_info))
        self.log.debug('Done doing on_run')
        return True

    def _find_objects_and_interactions(self) -> Tuple[Tuple[GameObject, Tuple[Interaction]]]:
        target_static_commodities = getattr(self, 'target_static_commodities', tuple())
        exclude_target_static_commodities = getattr(self, 'exclude_target_static_commodities', tuple())
        target_object_tags = getattr(self, 'target_object_tags', tuple())
        self.log.format(exclude_target_static_commodities=exclude_target_static_commodities, target_static_commodities=target_static_commodities, target_object_tags=target_object_tags)

        def _has_tag(_obj: GameObject) -> bool:
            if not target_object_tags:
                return True
            return CommonObjectTagUtils.has_game_tags(_obj, target_object_tags)

        found_objects = tuple(CommonObjectUtils.get_instance_for_all_visible_game_objects_generator(include_object_callback=_has_tag))
        self.log.format(found_objects=found_objects)

        def _has_commodity(_interaction: Interaction) -> bool:
            if not target_static_commodities:
                return False
            interaction_commodities = _interaction._static_commodities_set
            if not interaction_commodities:
                return False
            self.log.format(interaction=_interaction, interaction_short_name=CommonInteractionUtils.get_interaction_short_name(_interaction), static_commodities=interaction_commodities)
            for static_commodity in target_static_commodities:
                static_comm_guid = getattr(static_commodity.static_commodity, 'guid64', None)
                for commodity in interaction_commodities:
                    comm_guid = getattr(commodity.static_commodity, 'guid64', None)
                    if static_comm_guid == comm_guid:
                        return True
            return False

        def _exclude_has_commodity(_interaction: Interaction) -> bool:
            if not exclude_target_static_commodities:
                return True
            interaction_commodities = _interaction._static_commodities_set
            if not interaction_commodities:
                return False
            self.log.format(interaction=_interaction, interaction_short_name=CommonInteractionUtils.get_interaction_short_name(_interaction), static_commodities=interaction_commodities)
            for static_commodity in exclude_target_static_commodities:
                static_comm_guid = getattr(static_commodity.static_commodity, 'guid64', None)
                for commodity in interaction_commodities:
                    comm_guid = getattr(commodity.static_commodity, 'guid64', None)
                    if static_comm_guid == comm_guid:
                        return False
            return True

        include_interaction = CommonFunctionUtils.run_predicates_as_one((_has_commodity, _exclude_has_commodity))

        objects_and_interactions: List[Tuple[GameObject, Tuple[Interaction]]] = list()
        for found_object in found_objects:
            obj_interactions = tuple(CommonObjectInteractionUtils.get_all_interactions_registered_to_object_gen(found_object, include_interaction_callback=include_interaction))
            self.log.format(matching_interactions=obj_interactions)
            if not obj_interactions:
                continue
            objects_and_interactions.append((found_object, obj_interactions))

        return tuple(objects_and_interactions)
