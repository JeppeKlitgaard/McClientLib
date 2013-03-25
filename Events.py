from EventManager import EventManager, Event


def e(*names):
    event = Event()
    for name in names:
        event.add_name(name)

    return event


class BaseEventManager(EventManager):
    def __init__(self):
        super(BaseEventManager, self).__init__()

        self["recv00"] = e("recv_keepalive")
        self["sent00"] = e("sent_keepalive")

        self["recv01"] = e("recv_login_request")

        self["sent02"] = e("sent_handshake")

        self["recv03"] = e("recv_chat_message")
        self["sent03"] = e("sent_chat_message")

        self["recv04"] = e("recv_time_update")

        self["recv05"] = e("recv_entity_equipment")

        self["recv06"] = e("recv_spawn_position")

        self["sent07"] = e("sent_use_entity")

        self["recv08"] = e("recv_update_health")

        self["recv09"] = e("recv_respawn")

        self["recv0A"] = e("recv_player")

        self["sent0B"] = e("sent_player_position")

        self["sent0C"] = e("sent_player_look")

        self["recv0D"] = e("recv_player_position_and_look")
        self["sent0D"] = e("sent_player_position_and_look")

        self["sent0E"] = e("sent_player_digging")

        self["sent0F"] = e("sent_player_block_placement")

        self["recv10"] = e("recv_held_item_change")
        self["sent10"] = e("sent_held_item_change")

        self["recv11"] = e("recv_use_bed")

        self["recv12"] = e("recv_animation")
        self["sent12"] = e("sent_animation")

        self["sent13"] = e("sent_entity_action")

        self["recv14"] = e("recv_spawn_named_entity")

        self["recv16"] = e("recv_collect_item")

        self["recv17"] = e("recv_spawn_object")

        self["recv18"] = e("recv_spawn_mob")

        self["recv19"] = e("recv_spawn_painting")

        self["recv1A"] = e("recv_spawn_exp_orb")

        self["recv1C"] = e("recv_entity_velocity")

        self["recv1D"] = e("recv_destroy_entity")

        self["recv1E"] = e("recv_entity")

        self["recv1F"] = e("recv_entity_relative_move")

        self["recv20"] = e("recv_entity_look")

        self["recv21"] = e("recv_entity_look_and_relative_move")

        self["recv22"] = e("recv_entity_teleport")

        self["recv23"] = e("recv_entity_head_look")

        self["recv26"] = e("recv_entity_status")

        self["recv27"] = e("recv_attach_entity")

        self["recv28"] = e("recv_entity_metadata")

        self["recv29"] = e("recv_entity_effect")

        self["recv2A"] = e("recv_remove_entity_effect")

        self["recv2B"] = e("recv_set_exp")

        self["recv33"] = e("recv_chunk_data")

        self["recv34"] = e("recv_multi_block_change")

        self["recv35"] = e("recv_block_change")

        self["recv36"] = e("recv_block_action")

        self["recv37"] = e("recv_block_break_animation")

        self["recv38"] = e("recv_map_chunk_bulk")

        self["recv3C"] = e("recv_explosion")

        self["recv3D"] = e("recv_sound_or_particle_effect")

        self["recv3E"] = e("recv_named_sound_effect")

        self["recv3F"] = e("recv_particle")

        self["recv46"] = e("recv_change_game_state")

        self["recv47"] = e("recv_spawn_global_entity")

        self["recv64"] = e("recv_open_window")

        self["recv65"] = e("recv_close_window")
        self["sent65"] = e("sent_close_window")

        self["sent66"] = e("sent_click_window")

        self["recv67"] = e("recv_set_slot")

        self["recv68"] = e("recv_set_window_items")

        self["recv69"] = e("recv_update_window_property")

        self["recv6A"] = e("recv_confirm_transaction")
        self["sent6A"] = e("sent_confirm_transaction")

        self["recv6B"] = e("recv_creative_inventory_action")
        self["sent6B"] = e("sent_creative_inventory_action")

        self["sent6C"] = e("sent_enchant_item")

        self["recv82"] = e("recv_update_sign")
        self["sent82"] = e("sent_update_sign")

        self["recv83"] = e("recv_item_data")

        self["recv84"] = e("recv_update_tile_entity")

        self["recvC8"] = e("recv_increment_statistic")

        self["recvC9"] = e("recv_player_list_item")

        self["recvCA"] = e("recv_player_abilities")
        self["sentCA"] = e("sent_player_abilities")

        self["recvCB"] = e("recv_tab_complete")
        self["sentCB"] = e("sent_tab_complete")

        self["sentCC"] = e("sent_client_settings")

        self["sentCD"] = e("sent_client_statuses")

        self["recvCE"] = e("recv_scoreboard_objective")

        self["recvCF"] = e("recv_update_score")

        self["recvD0"] = e("recv_display_scoreboard")

        self["recvD1"] = e("recv_teams")

        self["recvFA"] = e("recv_plugin_message")

        self["sentFA"] = e("sent_plugin_message")

        self["recvFC"] = e("recv_encryption_key_response")
        self["sentFC"] = e("sent_encryption_key_response")

        self["recvFD"] = e("recv_encryption_key_request")

        self["sentFE"] = e("recv_client_list_ping")

        self["recvFF"] = e("recv_client_disconnect")
        self["sentFF"] = e("sent_client_disconnect")


class EventManager(BaseEventManager):
    def __init__(self, connection, *args, **kwargs):
        self.connection = connection
        super(EventManager, self).__init__(*args, **kwargs)

        self["recvFD"].add_handler(self.connection.respondFD)
        self["recvFC"].add_handler(self.connection.respondFC)
