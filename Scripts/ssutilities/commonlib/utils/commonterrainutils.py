"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, Union

import routing
import services.terrain_service
import terrain
from protocolbuffers.Math_pb2 import Vector3
from routing import SurfaceIdentifier
from interactions.context import InteractionContext
from objects.script_object import ScriptObject
from server.pick_info import PickType
from sims.sim_info import SimInfo
from sims4communitylib.utils.objects.common_object_location_utils import CommonObjectLocationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
import objects.terrain
import sims4.math


class CommonTerrainUtils:
    """ Utilities for the terrain. """
    @staticmethod
    def is_safe_route_surface_position(location_object: ScriptObject, interaction_context: InteractionContext):
        """ Determine if a position is a safe surface position. """
        if not CommonTypeUtils.is_terrain(location_object):
            return False
        if interaction_context is not None and interaction_context.pick is not None and isinstance(interaction_context.pick.pick_type, PickType):
            if interaction_context.pick.pick_type != PickType.PICK_TERRAIN and interaction_context.pick.pick_type != PickType.PICK_FLOOR:
                return False
            position = interaction_context.pick.location
            surface = interaction_context.pick.routing_surface
        else:
            position = location_object.position
            surface = location_object.routing_surface
        if surface is None or position is None:
            return False
        if interaction_context is None:
            return False
        sim = interaction_context.sim
        if sim is not None and CommonTypeUtils.is_sim_or_sim_info(sim):
            sim_info = CommonSimUtils.get_sim_info(sim)
            if sim_info is None:
                return False
            (lower_bound, _) = CommonTerrainUtils.get_wading_size(sim_info)
            if CommonTerrainUtils.get_water_depth_at(position.x, position.z, level=surface.secondary_id) > lower_bound:
                return False
        if not routing.test_point_placement_in_navmesh(surface, position):
            return False
        return True

    @staticmethod
    def get_wading_size(sim_info: SimInfo) -> Tuple[int, int]:
        """get_wading_size(sim_info)

        Retrieve the size of a Sim if they were to wade in a pool of water.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: A tuple indicating the x and y wading size of a Sim from their origin point.
        :rtype: Tuple[int, int]
        """
        # noinspection PyBroadException
        try:
            from world.ocean_tuning import OceanTuning
        except:
            return 0, 0
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return 0, 0
        wading_interval = OceanTuning.get_actor_wading_interval(sim)
        if wading_interval is None:
            return 0, 0
        return wading_interval.lower_bound, wading_interval.upper_bound

    @staticmethod
    def get_route_surface_position(script_object: ScriptObject) -> Vector3:
        """ Retrieve a safe surface position for an object. """
        return CommonObjectLocationUtils.get_position(script_object)

    @staticmethod
    def get_route_surface_position_from_interaction_context(interaction_context: InteractionContext) -> Union[Vector3, None]:
        """ Retrieve a surface position from an interaction context. """
        if interaction_context is None or interaction_context.pick is None:
            return None
        position = interaction_context.pick.location
        surface = interaction_context.pick.routing_surface
        position.y = CommonTerrainUtils.get_routing_surface_height_at(position.x, position.z, surface)
        return position

    @staticmethod
    def get_routing_surface_height_at(x: int, z: int, surface: SurfaceIdentifier) -> int:
        """ Determine the surface height for a surface. """
        return services.terrain_service.terrain_object().get_routing_surface_height_at(x, z, surface)

    @staticmethod
    def get_water_depth_at(x: int, z: int, level: int=0) -> int:
        """ Determine the water depth. """
        return terrain.get_water_depth(x, z, level=level)

    @staticmethod
    def get_route_surface_level(location_object: ScriptObject) -> int:
        """ Determine the surface level for an object. """
        return location_object.location.routing_surface.secondary_id

    @staticmethod
    def get_route_surface_level_from_interaction_context(interaction_context: InteractionContext) -> Union[int, None]:
        """ Retrieve a surface level from an interaction context. """
        if interaction_context is None or interaction_context.pick is None:
            return None
        return interaction_context.pick.routing_surface.secondary_id

    @staticmethod
    def build_terrain_target_and_context(sim_info: SimInfo, location_position: Vector3, surface_level: int) -> Tuple[Any, InteractionContext]:
        """ Build a terrain target and context. """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        from server_commands.sim_commands import _build_terrain_interaction_target_and_context
        sim = CommonSimUtils.get_sim_instance(sim_info)
        # noinspection PyUnresolvedReferences
        pos = sims4.math.Vector3(location_position.x, location_position.y, location_position.z)
        routing_surface = routing.SurfaceIdentifier(CommonLocationUtils.get_current_zone_id(), surface_level, routing.SurfaceType.SURFACETYPE_WORLD)
        return _build_terrain_interaction_target_and_context(sim, pos, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
