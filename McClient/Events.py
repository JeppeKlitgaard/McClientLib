from EventManager import EventManager, Event
import weakref.ref


class Ref(weakref.ref):
    def __getattribute__(self, name):
        return self().__getattribute__(name)


class BaseEventManager(EventManager):
    def set_event(self, name, *aliases):
        self[name] = Event()
        for alias in aliases:
            self.aliases[alias] = Ref(self[name])

    def __init__(self):
        super(BaseEventManager, self).__init__()
        self.aliases = {}

        self.set_event("recv00", "recv_keepalive")
        self.set_event("sent00", "sent_keepalive")

        self.set_event("recv01", "recv_login_request")

        self.set_event("sent02", "sent_handshake")

        self.set_event("recv03", "recv_chat_message")
        self.set_event("sent03", "sent_chat_message")

        self.set_event("recv04", "recv_time_update")

        self.set_event("recv05", "recv_entity_equipment")

        self.set_event("recv06", "recv_spawn_position")

        self.set_event("sent07", "sent_use_entity")

        self.set_event("recv08", "recv_update_health")

        self.set_event("recv09", "recv_respawn")

        self.set_event("recv0A", "recv_player")

        self.set_event("sent0B", "sent_player_position")

        self.set_event("sent0C", "sent_player_look")

        self.set_event("recv0D", "recv_player_position_and_look")
        self.set_event("sent0D", "sent_player_position_and_look")

        self.set_event("sent0E", "sent_player_digging")

        self.set_event("sent0F", "sent_player_block_placement")

        self.set_event("recv10", "recv_held_item_change")
        self.set_event("sent10", "sent_held_item_change")

        self.set_event("recv11", "recv_use_bed")

        self.set_event("recv12", "recv_animation")
        self.set_event("sent12", "sent_animation")

        self.set_event("sent13", "sent_entity_action")

        self.set_event("recv14", "recv_spawn_named_entity")

        self.set_event("recv16", "recv_collect_item")

        self.set_event("recv17", "recv_spawn_object")

        self.set_event("recv18", "recv_spawn_mob")

        self.set_event("recv19", "recv_spawn_painting")

        self.set_event("recv1A", "recv_spawn_exp_orb")

        self.set_event("recv1C", "recv_entity_velocity")

        self.set_event("recv1D", "recv_destroy_entity")

        self.set_event("recv1E", "recv_entity")

        self.set_event("recv1F", "recv_entity_relative_move")

        self.set_event("recv20", "recv_entity_look")

        self.set_event("recv21", "recv_entity_look_and_relative_move")

        self.set_event("recv22", "recv_entity_teleport")

        self.set_event("recv23", "recv_entity_head_look")

        self.set_event("recv26", "recv_entity_status")

        self.set_event("recv27", "recv_attach_entity")

        self.set_event("recv28", "recv_entity_metadata")

        self.set_event("recv29", "recv_entity_effect")

        self.set_event("recv2A", "recv_remove_entity_effect")

        self.set_event("recv2B", "recv_set_exp")

        self.set_event("recv33", "recv_chunk_data")

        self.set_event("recv34", "recv_multi_block_change")

        self.set_event("recv35", "recv_block_change")

        self.set_event("recv36", "recv_block_action")

        self.set_event("recv37", "recv_block_break_animation")

        self.set_event("recv38", "recv_map_chunk_bulk")

        self.set_event("recv3C", "recv_explosion")

        self.set_event("recv3D", "recv_sound_or_particle_effect")

        self.set_event("recv3E", "recv_named_sound_effect")

        self.set_event("recv3F", "recv_particle")

        self.set_event("recv46", "recv_change_game_state")

        self.set_event("recv47", "recv_spawn_global_entity")

        self.set_event("recv64", "recv_open_window")

        self.set_event("recv65", "recv_close_window")
        self.set_event("sent65", "sent_close_window")

        self.set_event("sent66", "sent_click_window")

        self.set_event("recv67", "recv_set_slot")

        self.set_event("recv68", "recv_set_window_items")

        self.set_event("recv69", "recv_update_window_property")

        self.set_event("recv6A", "recv_confirm_transaction")
        self.set_event("sent6A", "sent_confirm_transaction")

        self.set_event("recv6B", "recv_creative_inventory_action")
        self.set_event("sent6B", "sent_creative_inventory_action")

        self.set_event("sent6C", "sent_enchant_item")

        self.set_event("recv82", "recv_update_sign")
        self.set_event("sent82", "sent_update_sign")

        self.set_event("recv83", "recv_item_data")

        self.set_event("recv84", "recv_update_tile_entity")

        self.set_event("recvC8", "recv_increment_statistic")

        self.set_event("recvC9", "recv_player_list_item")

        self.set_event("recvCA", "recv_player_abilities")
        self.set_event("sentCA", "sent_player_abilities")

        self.set_event("recvCB", "recv_tab_complete")
        self.set_event("sentCB", "sent_tab_complete")

        self.set_event("sentCC", "sent_client_settings")

        self.set_event("sentCD", "sent_client_statuses")

        self.set_event("recvCE", "recv_scoreboard_objective")

        self.set_event("recvCF", "recv_update_score")

        self.set_event("recvD0", "recv_display_scoreboard")

        self.set_event("recvD1", "recv_teams")

        self.set_event("recvFA", "recv_plugin_message")
        self.set_event("sentFA", "sent_plugin_message")

        self.set_event("recvFC", "recv_encryption_key_response")
        self.set_event("sentFC", "sent_encryption_key_response")

        self.set_event("recvFD", "recv_encryption_key_request")

        self.set_event("sentFE", "recv_client_list_ping")

        self.set_event("recvFF", "recv_client_disconnect")
        self.set_event("sentFF", "sent_client_disconnect")

    def __getitem__(self, key):
        try:
            return super(BaseEventManager, self).__getitem__(key)
        except KeyError:
            return self.aliases[key]


class EventManager(BaseEventManager):
    def __init__(self, connection, *args, **kwargs):
        self.connection = connection
        super(EventManager, self).__init__(*args, **kwargs)

        self["recvFD"].add_handler(self.connection.respondFD)
        self["recvFC"].add_handler(self.connection.respondFC)
        self["recv00"].add_handler(self.connection.respond00)
