"""
Sim Snatcher is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import List

import services
import distributor.system
from drama_scheduler.drama_node_types import DramaNodeType
from objects import ALL_HIDDEN_REASONS
from protocolbuffers import InteractionOps_pb2, Consts_pb2
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from world import region
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_time_utils import CommonTimeUtils


class SSOrderToOperations:
    """ Utilities for ordering Sims. """
    @staticmethod
    def demand_sim_go_to_home_lot(sim_info: SimInfo, target_sim_info: SimInfo) -> bool:
        """ Demand a Sim to go to the home lot of a sim. """
        to_zone_id = CommonHouseholdUtils.get_household_lot_id(sim_info)
        if to_zone_id == services.current_zone_id():
            return False

        additional_sims = SSOrderToOperations._collect_always_travel_companions(sim_info)
        additional_sims.append(CommonSimUtils.get_sim_instance(target_sim_info))

        sim = sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
        travel_info = InteractionOps_pb2.TravelSimsToZone()
        travel_info.zone_id = to_zone_id
        # noinspection PyUnresolvedReferences
        travel_info.sim_ids.append(sim.id)
        travel_group = sim_info.travel_group
        if travel_group is not None and not any(sim_info is not sim_info and sim_info in sim_info.household for sim_info in travel_group):
            destination_region = region.get_region_instance_from_zone_id(to_zone_id)
            current_region = services.current_region()
            if not current_region.is_region_compatible(destination_region):
                services.travel_group_manager().destroy_travel_group_and_release_zone(travel_group, last_sim_info=sim_info)
        rabbit_hole_service = services.get_rabbit_hole_service()
        if rabbit_hole_service.is_in_rabbit_hole(sim.sim_id):
            rabbit_hole_service.set_ignore_travel_cancel_for_sim_id_in_rabbit_hole(sim.sim_id)
        sim.queue.cancel_all()
        for sim in additional_sims:
            sim.queue.cancel_all()
            # noinspection PyUnresolvedReferences
            travel_info.sim_ids.append(sim.sim_id)
        distributor.system.Distributor.instance().add_event(Consts_pb2.MSG_TRAVEL_SIMS_TO_ZONE, travel_info)
        CommonTimeUtils.pause_the_game()
        return True

    @staticmethod
    def _collect_always_travel_companions(sim_info: SimInfo) -> List[Sim]:
        additional_sims = list()
        drama_scheduler = services.drama_scheduler_service()
        if drama_scheduler is not None:
            drama_nodes = drama_scheduler.get_running_nodes_by_drama_node_type(DramaNodeType.TUTORIAL)
            if drama_nodes:
                tutorial_drama_node = drama_nodes[0]
                housemate_sim_info = tutorial_drama_node.get_housemate_sim_info()
                housemate_sim = housemate_sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
                if housemate_sim is not None and housemate_sim is not sim_info:
                    additional_sims.append(housemate_sim)
        selectable_sim_infos = CommonSimUtils.get_instanced_sim_info_for_all_sims_generator()
        if CommonSpeciesUtils.is_human(sim_info):
            if sum(1 for _sim_info in selectable_sim_infos if CommonSpeciesUtils.is_human(_sim_info) and CommonAgeUtils.is_older_than(_sim_info, Age.CHILD, or_equal=True)) == 1:
                additional_sims.extend([CommonSimUtils.get_sim_instance(_sim_info) for _sim_info in selectable_sim_infos if CommonSpeciesUtils.is_pet(_sim_info)])
            familiar_tracker = sim_info.sim_info.familiar_tracker
            if familiar_tracker is not None:
                active_familiar = familiar_tracker.get_active_familiar()
                if active_familiar is not None and active_familiar.is_sim:
                    additional_sims.append(active_familiar)
        return additional_sims
