import logging
from McLib.EventManager import Protocol_47
import re


class CustomFilter(logging.Filter):
    def set_up_filter(self, hide):
        self.hide = hide

    def filter(self, record):
        # Regex part
        regex = re.compile(r"^event([0-9DEFACB]{2})\| ")  # Regex
        event = re.match(regex, record.msg)  # Grab event
        if event:
            event = event.group(1)  # Make into string

        # Filter part

        if event in self.hide:
            return False
        return True


class DebugEventManager(Protocol_47):
    def __init__(self, custom_filter):
        super(DebugEventManager, self).__init__()

        self.custom_filter = custom_filter

        self.logger = logging.getLogger("DVM")
        self.file_handler = logging.FileHandler("DVM.log")
        self.stream_handler = logging.StreamHandler()

        self.formatter = logging.Formatter(
            '%(asctime)s %(message)s')

        self.file_handler.setFormatter(self.formatter)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        self.logger.setLevel(logging.INFO)
        self.logger.addFilter(self.custom_filter)

        self.logger.info("Started logging.")

    def event00(self, direct, kAid):
        self.logger.info("event00| (%s) kAid: %s", direct, kAid)

    def event01(self, direct, entityID, level_type, game_mode, dimension,
                difficulty, maxPlayers):
        self.logger.info("event01| (%s) entityID: %s, level_type: %s, "
                         "game_mode: %s, dimension: %s, difficulty: %s, "
                         "max_players: %s",
                         direct, entityID, level_type, game_mode,
                         dimension, difficulty, maxPlayers)

    def event02(self, direct, protocol_version, username, host, port):
        self.logger.info("event02| (%s) protocol_version: %s, username: %s, "
                         "host: %s, port:%s", direct, protocol_version,
                         username, host, port)

    def event03(self, direct, message):
        self.logger.info("event03| (%s) message: %s", direct, message)

    def event04(self, direct, world_age, time):
        self.logger.info("event04| (%s) time: %s, world_age: %s",
                         world_age, direct, time)

    def event05(self, direct, entityID, slot, item):
        self.logger.info("event05| (%s) entityID: %s, slot: %s, item: %s",
                         direct, entityID, slot, item)
        print item.return_tree()

    def event06(self, direct, x, y, z):
        self.logger.info("event06| (%s) x: %s, y: %s, z: %s", direct,
                         x, y, z)

    def event07(self, direct, user, target, mButton):
        self.logger.info("event07| (%s) user: %s, target: %s, mButton: %s"
                         % (direct, user, target, mButton))

    def event08(self, direct, health, food, saturation):
        self.logger.info("event08| (%s) health: %s, food: %s, saturation: %s",
                         direct, health, food, saturation)

    def event09(self, direct, dimension, difficulty, game_mode, height,
                level_type):
        self.logger.info("event09| (%s) dimension: %s, difficulty: %s, "
                         "game_mode: %s height: %s, level_type: %s",
                         direct, dimension, difficulty,
                         game_mode, height, level_type)

    def event0A(self, direct, on_ground):
        self.logger.info("event0A| (%s) on_ground: %s", direct, on_ground)

    def event0B(self, direct, x, y, stance, z, on_ground):
        self.logger.info("event0B| (%s) x: %s, y: %s, stance: %s, z: %s, "
                         "on_ground: %s", direct, x, y, stance, z, on_ground)

    def event0C(self, direct, yaw, pitch, on_ground):
        self.logger.info("event0C| (%s) yaw: %s, pitch: %s, on_ground: %s",
                         direct, yaw, pitch, on_ground)

    def event0D(self, direct, x, stance, y, z, yaw, pitch, onGround):
        self.logger.info("event0D| (%s) x: %s, stance: %s, y: %s, z: %s, "
                         "yaw: %s, pitch: %s, onGround: %s",
                         direct, x, stance, y, z, yaw, pitch, onGround)

    def event0E(self, direct, status, x, y, z, face):
        self.logger.info("event0E| (%s) status: %s, x: %s, y: %s, z: %s, "
                         "face: %s", status, x, y, z, face)

    def event0F(self, direct, x, y, z, direction, held, cpx, cpy, cpz):
        self.logger.info("event0F| (%s) x: %s, y: %s, z: %s, direction: %s, "
                         "held: %s, cpx: %s, cpy: %s, cpz: %s",
                         direct, x, y, z, direction, held, cpx, cpy, cpz)

    def event10(self, direct, slot):
        self.logger.info("event10| (%s) slot: %s", direct, slot)

    def event11(self, direct, entityID, x, y, z):
        self.logger.info("event11| (%s) entityID: %s, x: %s, y: %s, z: %s",
                         direct, entityID, x, y, z)

    def event12(self, direct, entityID, animationID):
        self.logger.info("event12| (%s) entityID: %s, animationID: %s",
                         direct, entityID, animationID)

    def event13(self, direct, entityID, actionID):
        self.logger.info("event13| (%s) entityID: %s, actionID: %s",
                         direct, entityID, actionID)

    def event14(self, direct, entityID, playerName, x, y, z, yaw, pitch,
                curItem, metadata):
        self.logger.info("event14| (%s) entityID: %s, playerName: %s, x: %s, "
                         "y: %s, z: %s, yaw: %s, pitch: %s, curItem: %s, "
                         "metadata: %s", direct, entityID, playerName,
                         x, y, z, yaw, pitch, curItem, metadata)

    def event15(self, direct, entityID, item, x, y, z,
                rotation, pitch, roll):
        self.logger.info("event15| (%s) entityID: %s, item: %s, "
                         "x: %s, y: %s, z: %s, "
                         "rotation: %s, pitch: %s, roll: %s", direct,
                         entityID, item, x, y, z, rotation, pitch, roll)

    def event16(self, direct, collectedID, collectorID):
        self.logger.info("event16| (%s) collectedID: %s, collectorID: %s",
                         direct, collectedID, collectorID)

    def event17(self, direct, entityID, type, x, y, z,
                throwerEntityID=None, speedX=None, speedY=None, speedZ=None):
        self.logger.info("event17| (%s) entityID: %s, type: %s, x: %s, y: %s, "
                         "z: %s, throwerEntityID: %s, speedX: %s, "
                         "speedY: %s, speedZ: %s", direct, entityID, type,
                         x, y, z, throwerEntityID, speedX, speedY, speedZ)

    def event18(self, direct, entityID, type, x, y, z, yaw, pitch, headYaw,
                metadata, velocityX, velocityY, velocityZ):
        self.logger.info("event18| (%s) entityID: %s, type: %s, x: %s, y: %s, "
                         "z: %s, yaw: %s, pitch: %s, headYaw: %s, "
                         "metadata: %s, velocityX: %s, velocityY: %s, "
                         "velocityZ: %s", direct, entityID, type, x, y, z,
                         yaw, pitch, headYaw, metadata,
                         velocityX, velocityY, velocityZ)

    def event19(self, direct, entityID, title, x, y, z, direction):
        self.logger.info("event19| (%s) entityID: %s, title: %s, "
                         "x: %s, y: %s, z: %s, direction: %s",
                         direct, entityID, title, x, y, z, direction)

    def event1A(self, direct, entityID, x, y, z, count):
        self.logger.info("event1A| (%s) entityID: %s, x: %s, y: %s, z: %s, "
                         "count: %s", direct, entityID, x, y, z, count)

    def event1C(self, direct, entityID, velocityX, velocityY, velocityZ):
        self.logger.info("event1C| (%s) entityID: %s, velocityX: %s, "
                         "velocityY: %s, velocityZ: %s",
                         direct, entityID, velocityX, velocityY, velocityZ)

    def event1D(self, direct, entities):
        self.logger.info("event1D| (%s) entities: %s", direct, entities)

    def event1E(self, direct, entityID):
        self.logger.info("event1E| (%s) entityID: %s", direct, entityID)

    def event1F(self, direct, entityID, x, y, z):
        self.logger.info("event1F| (%s) entityID: %s, x: %s, y: %s, z: %s",
                         direct, entityID, x, y, z)

    def event20(self, direct, entityID, yaw, pitch):
        self.logger.info("event20| (%s) entityID: %s, yaw: %s, pitch: %s",
                         direct, entityID, yaw, pitch)

    def event21(self, direct, entityID, x, y, z, yaw, pitch):
        self.logger.info("event21| (%s) entityID: %s, x: %s, y: %s, z: %s, "
                         "yaw: %s, pitch: %s", direct, entityID, x, y, z,
                         yaw, pitch)

    def event22(self, direct, entityID, x, y, z, yaw, pitch):
        self.logger.info("event22| (%s) entityID: %s, x: %s, y: %s, z: %s, "
                         "yaw: %s, pitch: %s", direct, entityID, x, y, z,
                         yaw, pitch)

    def event23(self, direct, entityID, headYaw):
        self.logger.info("event23| (%s) entityID: %s, headYaw: %s",
                         direct, entityID, headYaw)

    def event26(self, direct, entityID, status):
        self.logger.info("event26| (%s) entityID: %s, status: %s",
                         direct, entityID, status)

    def event27(self, direct, entityID, vehicleID):
        self.logger.info("event27| (%s) entityID: %s, vehicleID: %s",
                         direct, entityID, vehicleID)

    def event28(self, direct, entityID, metadata):
        self.logger.info("event28| (%s) entityID: %s, metadata: %s",
                         direct, entityID, metadata)

    def event29(self, direct, entityID, effectID, amplifier, duration):
        self.logger.info("event29| (%s) entityID: %s, "
                         "effectID: %s, amplifier: %s, duration: %s",
                         direct, entityID, effectID, amplifier, duration)

    def event2A(self, direct, entityID, effectID):
        self.logger.info("event2A| (%s) entityID: %s, effectID: %s",
                         direct, entityID, effectID)

    def event2B(self, direct, expBar, level, totalExp):
        self.logger.info("event2B| (%s) expBar: %s, level: %s, totalExp: %s",
                         direct, expBar, level, totalExp)

    def event33(self, direct, x, z):
        self.logger.info("event33| (%s) x: %s, z: %s", direct, x, z)

    def event34(self, direct, chunkX, chunkZ, affectedBlocks):
        self.logger.info("event34| (%s) chunkX: %s, chunkZ: %s, "
                         "affectedBlocks: %s", direct,
                         chunkX, chunkZ, affectedBlocks)

    def event35(self, direct, x, y, z, blockType, metadata):
        self.logger.info("event35| (%s) x: %s, y: %s: z: %s, blockType: %s, "
                         "metadata: %s", direct, x, y, z,
                         blockType, metadata)

    def event36(self, direct, x, y, z, byte1, byte2, blockID):
        self.logger.info("event36| (%s) x: %s, y: %s, z: %s, "
                         "byte1: %s, byte2: %s, blockID: &s",
                         direct, x, y, z, byte1, byte2, blockID)

    def event37(self, direct, entityID, x, y, z, destroyedStage):
        self.logger.info("event37| (%s) entityID: %s, x: %s, y: %s, z: %s, "
                         "destroyedStage: %s", direct, entityID, x, y, z,
                         destroyedStage)

    def event38(self, direct, chunkCount):
        self.logger.info("event38| (%s) chunkCount: %s",
                         direct, chunkCount)

    def event3C(self, direct, x, y, z, radius, affectedBlocks):
        self.logger.info("event3C| (%s) x: %s, y: %s, z: %s, radius: %s, "
                         "affectedBlocks: %s", direct, x, y, z, radius,
                         affectedBlocks)

    def event3D(self, direct, effectID, x, y, z, data, no_volume_decrease):
        self.logger.info("event3D| (%s) effectID: %s, x: %s, y: %s, z: %s, "
                         "data: %s, no_volume_decrease: %s", direct,
                         effectID, x, y, z, data, no_volume_decrease)

    def event3E(self, direct, sound, x, y, z, volume, pitch):
        self.logger.info("event3E| (%s) sound: %s, x: %s, y: %s, z: %s, "
                         "volume: %s, pitch: %s", direct, sound, x, y, z,
                         volume, pitch)

    def event46(self, direct, reason, gamemode):
        self.logger.info("event46| (%s) reason: %s, gamemode: %s", direct,
                         reason, gamemode)

    def event47(self, direct, entityID, x, y, z):
        self.logger.info("event47| (%s) entityID: %s, x: %s, y: %s, z: %s",
                         direct, entityID, x, y, z)

    def event64(self, direct, windowID, inventoryType, windowTitle,
                numberOfSlots):
        self.logger.info("event64| (%s) windowID: %s, inventoryType: %s, "
                         "windowTitle: %s, numberOfSlots: %s",
                         direct, windowID, inventoryType, windowTitle,
                         numberOfSlots)

    def event65(self, direct, windowID):
        self.logger.info("event65| (%s) windowID: %s", direct, windowID)

    def event66(self, direct, window_id, slot, mButton, action_number,
                shift, clicked_item):
        self.logger.info("event66| (%s) window_id: %s, slot: %s, "
                         "mButton: %s, action_number: %s, shift: %s, "
                         "clicked_item: %s", direct, window_id, slot,
                         mButton, action_number, shift, clicked_item)

    def event67(self, direct, windowID, slot, slotData):
        self.logger.info("event67| (%s) windowID: %s, slot: %s, slotData: %s",
                         direct, windowID, slot, slotData)

    def event68(self, direct, windowID, count, slots):
        self.logger.info("event68| (%s) windowID: %s, count: %s, slots: %s",
                         direct, windowID, count, slots)

    def event69(self, direct, windowID, property, value):
        self.logger.info("event69| (%s) windowID: %s, property: %s, value: %s",
                         direct, windowID, property, value)

    def event6A(self, direct, windowID, actionType, accepted):
        self.logger.info("event6A| (%s) windowID: %s, actionType: %s, "
                         "accepted: %s", direct, windowID,
                         actionType, accepted)

    def event6B(self, direct, slot, clickedItem):
        self.logger.info("event6B| (%s) slot: %s, clickedItem: %s",
                         direct, slot, clickedItem)

    def event6C(self, direct, window_id, enchantment):
        self.logger.info("event6C| (%s) window_id: %s, enchantment: %s",
                         direct, window_id, enchantment)

    def event82(self, direct, x, y, z, line1, line2, line3, line4):
        self.logger.info("event82| (%s) x: %s, y: %s, z: %s, line1: %s, "
                         "line2: %s, line3: %s, line4: %s", direct, x, y, z,
                         line1, line2, line3, line4)

    def event83(self, direct, itemType, itemID, text):
        self.logger.info("event83| (%s) itemType: %s, itemID: %s, text: %s",
                         direct, itemType, itemID, text)

    def event84(self, direct, x, y, z, action, nbtData=None):
        self.logger.info("event84| (%s) x: %s, y: %s, z: %s, action: %s",
                         direct, x, y, z, action)

    def eventC8(self, direct, statID, amount):
        self.logger.info("eventC8| (%s) statID: %s, amount: %s",
                         direct, statID, amount)

    def eventC9(self, direct, playerName, online, ping):
        self.logger.info("eventC9| (%s) playerName: %s, online: %s, ping: %s",
                         direct, playerName, online, ping)

    def eventCA(self, direct, flags, flySpeed, walkSpeed):
        self.logger.info("eventCA| (%s) flags: %s, flySpeed: %s, "
                         "walkSpeed: %s", direct, flags, flySpeed, walkSpeed)

    def eventCB(self, direct, text):
        self.logger.info("eventCB| (%s) text: %s", direct, text)

    def eventCC(self, direct, locale, view_distance, chat_flags, difficulty,
                show_cape):
        self.logger.info("eventCC| (%s) locale: %s, view_distance: %s, "
                         "chat_flags: %s, difficulty: %s, show_cape: %s",
                         direct, locale, view_distance, chat_flags,
                         difficulty, show_cape)

    def eventCD(self, direct, payload):
        self.logger.info("eventCD| (%s) payload: %s", direct, payload)

    def eventFA(self, direct, channel, message):
        self.logger.info("eventFA| (%s) channel: %s, message: %s", direct,
                         channel, message)

    def eventFC(self, direct, sharedSecret, token):
        self.logger.info("eventFC| (%s)", direct)

    def eventFD(self, direct, serverID, publicKey, token):
        self.logger.info("eventFD| (%s) serverID: %s", direct, serverID)

    def eventFF(self, direct, reason):
        self.logger.info("eventFF| (%s) reason: %s", direct, reason)

    def event_protocol_error(self, response):
        self.logger.info("event_protocol_error| response: %s", response)

    def event_socket_connected(self, host, port):
        self.logger.info("event_socket_connected| host: %s, port: %s",
                         host, port)

    def event_generated_shared_secret(self, shared_secret):
        self.logger.info("event_generated_shared_secret")

    def event_protocol_kick(self, reason):
        self.logger.info("event_protocol_kick| reason: %s", reason)

    def event_insane_packet(self, packetid):
        self.logger.info("event_insane_packet| packetid: %s", packetid)

    def event_encryption_enabled(self):
        self.logger.info("event_encryption_enabled")

    def event_session_joinserver(self):
        self.logger.info("event_session_joinserver")

    def event_server_mode(self, mode):  # True = online, False = offline
        self.logger.info("event_server_mode: server mode is online: %s" % mode)