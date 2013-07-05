from Utils import hex2str


class BaseSender(object):
    """Base class for Senders."""
    protocol_version = 0

    def __init__(self, connection):
        self.connection = connection

    def write_id(self, pid):
        self.connection.write_id(pid)
        self.connection.eventmanager["sent" + hex2str(pid)]()


class Sender(BaseSender):
    protocol_version = 61

    def send_keepalive(self, KID):
        self.write_id("\x00")
        self.connection.write_int(KID)

    def send_handshake(self):
        self.write_id("\x02")
        self.connection.write_byte(self.protocol_version)
        self.connection.write_string(self.connection.session.username)
        self.connection.write_string(self.connection.host)
        self.connection.write_int(self.connection.port)

    def send_chat_message(self, message):
        self.write_id("\x03")
        if not message:
            raise TypeError("'message' must be string of atleast 1 character")
        self.connection.write_string(message)

    def send_use_entity(self, EID, targetID, button):
        self.write_id("\x07")
        self.connection.write_int(EID)
        self.connection.write_int(targetID)
        self.connection.write_boolean(button)

    def send_player_flying(self, on_ground):
        self.write_id("\x0A")
        self.connection.write_boolean(on_ground)

    def send_player_position(self, x, y, stance, z, on_ground):
        self.write_id("\x0B")
        self.connection.write_double(x)
        self.connection.write_double(y)
        self.connection.write_double(stance)
        self.connection.write_double(z)
        self.connection.write_boolean(on_ground)

    def send_player_look(self, yaw, pitch, on_ground):
        self.write_id("\x0C")
        self.connection.write_float(yaw)
        self.connection.write_float(pitch)
        self.connection.write_boolean(on_ground)

    def send_player_position_and_look(self, x, y, stance, z, yaw, pitch,
                                      on_ground):
        self.write_id("\x0D")
        self.connection.write_double(x)
        self.connection.write_double(y)
        self.connection.write_double(stance)
        self.connection.write_double(z)
        self.connection.write_float(yaw)
        self.connection.write_float(pitch)
        self.connection.write_boolean(on_ground)

    def send_player_digging(self, status, x, y, z, face):
        self.write_id("\x0E")
        self.connection.write_byte(status)
        self.connection.write_int(x)
        self.connection.write_byte(y)
        self.connection.write_int(z)
        self.connection.write_byte(face)

    def send_player_block_placement(self, x, y, z, direction, held_item,
                                    cursor_x, cursor_y, cursor_z):
        self.write_id("\x0F")
        self.connection.write_int(x)
        self.connection.write_ubyte(y)
        self.connection.write_int(z)
        self.connection.write_byte(direction)
        self.connection.write_slot(held_item)  # TODO Implement write_slot
        self.connection.write_byte(cursor_x)
        self.connection.write_byte(cursor_y)
        self.connection.write_byte(cursor_z)

    def send_held_item_change(self, slotID):
        self.write_id("\x10")
        self.connection.write_short(slotID)

    def send_animation(self, EID, animation):
        self.write_id("\x12")
        self.connection.write_int(EID)
        self.connection.write_byte(animation)

    def send_entity_action(self, EID, actionID):
        self.write_id("\x13")
        self.connection.write_int(EID)
        self.connection.write_byte(actionID)

    def send_close_window(self, windowID):
        self.write_id("\x65")
        self.connection.write_byte(windowID)

    def send_click_window(self, windowID, slot, button, actionID, mode,
                          clicked_item):
        self.write_id("\x66")
        self.connection.write_byte(windowID)
        self.connection.write_short(slot)
        self.connection.write_byte(button)
        self.connection.write_short(actionID)
        self.connection.write_byte(mode)
        self.connection.write_slot(clicked_item)  # TODO fix write_slot

    def send_confirm_transaction(self, windowID, actionID, accepted):
        self.write_id("\x6A")
        self.connection.write_byte(windowID)
        self.connection.write_short(actionID)
        self.connection.write_boolean(accepted)

    def send_creative_inventory_action(self, slot, clicked_item):
        self.write_id("\x6B")
        self.connection.write_short(slot)
        self.connection.write_slot(clicked_item)  # TODO fix write_slot

    def send_enchant_item(self, windowID, enchantment):
        self.write_id("\x6C")
        self.connection.write_byte(windowID)
        self.connection.write_byte(enchantment)

    def send_update_sign(self, x, y, z, line1, line2, line3, line4):
        self.write_id("\x82")
        self.connection.write_int(x)
        self.connection.write_short(y)
        self.connection.write_int(z)
        self.connection.write_string(line1)
        self.connection.write_string(line2)
        self.connection.write_string(line3)
        self.connection.write_string(line4)

    def send_player_abilities(self, flags, flying_speed, walking_speed):
        self.write_id("\xCA")
        self.connection.write_byte(flags)
        self.connection.write_byte(flying_speed)
        self.connection.write_byte(walking_speed)

    def send_tab_complete(self, text):
        self.write_id("\xCB")
        self.connection.write_string(text)

    def send_client_settings(self, locale, view_distance, chat_flags,
                             difficulty, show_cape):
        self.write_id("\xCC")
        self.connection.write_string(locale)
        self.connection.write_byte(view_distance)
        self.connection.write_byte(chat_flags)
        self.connection.write_byte(difficulty)
        self.connection.write_boolean(show_cape)

    def send_client_status(self, payload):
        self.write_id("\xCD")
        self.connection.write_byte(payload)

    def send_plugin_message(self, channel, data):
        self.write_id("\xFA")
        self.connection.write_string(channel)
        self.connection.write_bytearray(data)

    def send_encryption_key_response(self, secret, token):
        self.write_id("\xFC")
        self.connection.write_bytearray(secret)
        self.connection.write_bytearray(token)

    def send_client_list_ping(self, magic=1):
        self.write_id("\xFE")
        self.connection.write_byte(magic)

    def send_disconnect(self, reason):
        self.write_id("\xFF")
        self.connection.write_string(reason)
