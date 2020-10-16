"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import routing
import objects.terrain
from typing import Union, Tuple

from objects.game_object import GameObject
from interactions.context import InteractionContext
from server.pick_info import PickType
from sims.sim_info import SimInfo
from sims4communitylib.classes.math.common_surface_identifier import CommonSurfaceIdentifier
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from sims4communitylib.utils.location.common_terrain_utils import CommonTerrainUtils
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.sims.common_sim_body_utils import CommonSimBodyUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class SSCommonTerrainUtils:
    """ Utilities for the terrain. """
    @staticmethod
    def is_safe_route_surface_position(game_object: GameObject, interaction_context: InteractionContext):
        """ Determine if a position is a safe surface position. """
        if not CommonTypeUtils.is_terrain(game_object):
            return False
        if interaction_context is not None and interaction_context.pick is not None and isinstance(interaction_context.pick.pick_type, PickType):
            if interaction_context.pick.pick_type != PickType.PICK_TERRAIN and interaction_context.pick.pick_type != PickType.PICK_FLOOR:
                return False
            position = CommonVector3.from_vector3(interaction_context.pick.location)
            routing_surface = CommonSurfaceIdentifier.from_surface_identifier(interaction_context.pick.routing_surface)
        else:
            position = CommonObjectLocationUtils.get_position(game_object)
            routing_surface = CommonObjectLocationUtils.get_routing_surface(game_object)
        if routing_surface is None or position is None:
            return False
        if interaction_context is None:
            return False
        sim_info = CommonSimUtils.get_sim_info(interaction_context.sim)
        if sim_info is None:
            return False
        (lower_bound, _) = CommonSimBodyUtils.get_wading_size(sim_info)
        if CommonTerrainUtils.get_water_depth_at(position.x, position.z, surface_level=routing_surface.secondary_id) > lower_bound:
            return False
        if not CommonLocationUtils.can_position_be_routed_to(position, routing_surface):
            return False
        return True

    @staticmethod
    def get_route_surface_position_from_interaction_context(interaction_context: InteractionContext) -> Union[CommonVector3, None]:
        """ Retrieve a surface position from an interaction context. """
        if interaction_context is None or interaction_context.pick is None:
            return None
        position = interaction_context.pick.location
        surface = interaction_context.pick.routing_surface
        position.y = CommonLocationUtils.get_surface_height_at(position.x, position.z, surface)
        return position

    @staticmethod
    def get_route_surface_level_from_interaction_context(interaction_context: InteractionContext) -> Union[int, None]:
        """ Retrieve a surface level from an interaction context. """
        if interaction_context is None or interaction_context.pick is None:
            return None
        return interaction_context.pick.routing_surface.secondary_id

    @staticmethod
    def build_terrain_target_and_context(sim_info: SimInfo, position: CommonVector3, level: int) -> Tuple[objects.terrain.TerrainPoint, InteractionContext]:
        """ Build a target and a context for the terrain. """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        from server_commands.sim_commands import _build_terrain_interaction_target_and_context
        sim = CommonSimUtils.get_sim_instance(sim_info)
        routing_surface = CommonSurfaceIdentifier(CommonLocationUtils.get_current_zone_id(), secondary_id=level, surface_type=routing.SurfaceType.SURFACETYPE_WORLD)
        return _build_terrain_interaction_target_and_context(sim, position, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
