from Exceptions import HandlerError, ConnectionClosed

FIXME = "FIXME"


class BaseReceiver(object):
    """Base class for Receivers."""
    protocol_version = 0

    def __init__(self, connection):
        self.connection = connection

    def _get_handler(self, pid):
        try:
            return getattr(self, "handle" + pid)
        except AttributeError:
            if not pid:
                raise ConnectionClosed("Server terminated connection.")

            raise HandlerError("Object has no handler '%s'" % pid)

    def data_received(self):
        pid = self.connection.read_id()
        handler = self._get_handler(pid)
        data = handler()
        self.connection.eventmanager["recv" + pid](**data)


class Receiver(BaseReceiver):
    protocol_version = 60

    def handle00(self):
        KID = self.connection.read_int()
        toReturn = {"KID": KID}

        return toReturn

    def handle01(self):
        EID = self.connection.read_int()
        level_type = self.connection.read_string()
        game_mode = self.connection.read_byte()
        dimension = self.connection.read_byte()
        difficulty = self.connection.read_byte()
        self.connection.read_byte()  # Unused
        max_players = self.connection.read_byte()
        toReturn = {'EID': EID,
                    'level_type': level_type,
                    'game_mode': game_mode,
                    'dimension': dimension,
                    'difficulty': difficulty,
                    'max_players': max_players
                    }

        return toReturn

    def handle03(self):
        message = self.connection.read_string()
        toReturn = {"message": message}

        return toReturn

    def handle04(self):
        world_age = self.connection.read_long()
        time = self.connection.read_long()
        toReturn = {"world_age": world_age,
                    "time": time}

        return toReturn

    def handle05(self):
        EID = self.connection.read_int()
        slot = self.connection.read_short()
        item = FIXME
        toReturn = {"EID": EID,
                    "slot": slot,
                    "item": item}

        return toReturn

    def handle06(self):
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        toReturn = {"x": x,
                    "y": y,
                    "z": z}

        return toReturn

    def handle08(self):
        health = self.connection.read_short()
        food = self.connection.read_short()
        saturation = self.connection.read_float()
        toReturn = {"health": health,
                    "food": food,
                    "saturation": saturation}

        return toReturn

    def handle09(self):
        dimension = self.connection.read_int()
        difficulty = self.connection.read_byte()
        game_mode = self.connection.read_byte()
        height = self.connection.read_short()
        level_type = self.connection.read_string()
        toReturn = {"dimension": dimension,
                    "difficulty": difficulty,
                    "game_mode": game_mode,
                    "height": height,
                    "level_type": level_type}

        return toReturn

    def handle0D(self):
        x = self.connection.read_double()
        stance = self.connection.read_double()
        y = self.connection.read_double()
        z = self.connection.read_double()
        yaw = self.connection.read_float()
        pitch = self.connection.read_float()
        on_ground = self.connection.read_boolean()
        toReturn = {"x": x,
                    "stance": stance,
                    "y": y,
                    "z": z,
                    "yaw": yaw,
                    "pitch": pitch,
                    "on_ground": on_ground}

        return toReturn

    def handle10(self):
        slotID = self.connection.read_short()
        toReturn = {"slotID": slotID}

        return toReturn

    def handle11(self):
        EID = self.connection.read_int()
        self.connection.read_byte()  # Unused
        x = self.connection.read_int()
        y = self.connection.read_byte()
        z = self.connection.read_int()
        toReturn = {"EID": EID,
                    "x": x,
                    "y": y,
                    "z": z}

        return toReturn

    def handle12(self):
        EID = self.connection.read_int()
        animationID = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "animationID": animationID}

        return toReturn

    def handle14(self):
        EID = self.connection.read_int()
        player_name = self.connection.read_string()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        yaw = self.connection.read_byte()  # Wiki says byte, not float
        pitch = self.connection.read_byte()  # Changed it
        held_item = self.connection.read_short()
        metadata = FIXME
        toReturn = {'EID': EID,
                    'player_name': player_name,
                    'x': x,
                    'y': y,
                    'z': z,
                    'yaw': yaw,
                    'pitch': pitch,
                    'held_item': held_item,
                    'metadata': metadata
                    }

        return toReturn

    def handle16(self):
        collectedID = self.connection.read_int()
        collectorID = self.connection.read_int()
        toReturn = {"collectedID": collectedID,
                    "collectorID": collectorID}

        return toReturn

    def handle17(self):
        EID = self.connection.read_int()
        type = self.connection.read_byte()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        pitch = self.connection.read_byte()
        yaw = self.connection.read_byte()
        ThrowerEntityID = self.connection.read_int()
        if(ThrowerEntityID > 0):  #TODO Object data reader. also fix this.
            SpeedX = self.connection.read_short()
            SpeedY = self.connection.read_short()
            SpeedZ = self.connection.read_short()
            toReturn = {"entityID": EntityID,
                        "type": Type,
                        "x": x,
                        "y": y,
                        "z": z,
                        "throwerEntityID": ThrowerEntityID,
                        "speedX": SpeedX,
                        "speedY": SpeedY,
                        "speedZ": SpeedZ}
            return toReturn
        else:
            toReturn = {"entityID": EntityID,
                        "type": Type,
                        "x": x,
                        "y": y,
                        "z": z}
            return toReturn

    def handle18(self):
        EID = self.connection.read_int()
        type = self.connection.read_byte()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        pitch = self.connection.read_byte()
        head_pitch = self.connection.read_byte()
        yaw = self.connection.read_byte()
        velocityX = self.connection.read_short()
        velocityY = self.connection.read_short()
        velocityZ = self.connection.read_short()
        metadata = FIXME

        toReturn = {"EID": EID,
                    "type": type,
                    "x": x,
                    "y": y,
                    "z": z,
                    "pitch": pitch,
                    "head_pitch": head_pitch,
                    "yaw": yaw,
                    "velocityX": VelocityX,
                    "velocityY": VelocityY,
                    "velocityZ": VelocityZ,
                    "metadata": metadata}

        return toReturn

    def handle19(self):
        EID = self.connection.read_int()
        title = self.connection.read_string()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        direction = self.connection.read_int()
        toReturn = {"EID": EID,
                    "title": title,
                    "x": x,
                    "y": y,
                    "z": z,
                    "direction": direction}
        return toReturn

    def handle1A(self):
        EID = self.connection.read_int()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        count = self.connection.read_short()
        toReturn = {"EID": EID,
                    "x": x,
                    "y": y,
                    "z": z,
                    "count": count}

        return toReturn

    def handle1C(self):
        EID = self.connection.read_int()
        velocityX = self.connection.read_short()
        velocityY = self.connection.read_short()
        velocityZ = self.connection.read_short()
        toReturn = {"EID": EID,
                    "velocityX": velocityX,
                    "velocityY": velocityY,
                    "velocityZ": velocityZ}

        return toReturn

    def handle1D(self):  # TODO FIX LATER
        EntityArrayLength = self.connection.read_byte()
        Entities = []
        for i in range(EntityArrayLength):
            Entities.append(self.connection.read_int())

        toReturn = {"entities": Entities}
        return toReturn

    def handle1E(self):
        EID = self.connection.read_int()

        toReturn = {"EID": EID}

        return toReturn

    def handle1F(self):
        EID = self.connection.read_int()
        x = self.connection.read_byte()
        y = self.connection.read_byte()
        z = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "x": x,
                    "y": y,
                    "z": z}

        return toReturn

    def handle20(self):
        EID = self.connection.read_int()
        yaw = self.connection.read_byte()
        pitch = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "yaw": yaw,
                    "pitch": pitch}

        return toReturn

    def handle21(self):
        EID = self.connection.read_int()
        x = self.connection.read_byte()
        y = self.connection.read_byte()
        z = self.connection.read_byte()
        yaw = self.connection.read_byte()
        pitch = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "x": x,
                    "y": y,
                    "z": z,
                    "yaw": yaw,
                    "pitch": pitch}

        return toReturn

    def handle22(self):
        EID = self.connection.read_int()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        yaw = self.connection.read_byte()
        pitch = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "x": x,
                    "y": y,
                    "z": z,
                    "yaw": yaw,
                    "pitch": pitch}

        return toReturn

    def handle23(self):
        EID = self.connection.read_int()
        head_yaw = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "head_yaw": head_yaw}

        return toReturn

    def handle26(self):
        EID = self.connection.read_int()
        status = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "status": status}

        return toReturn

    def handle27(self):
        EID = self.connection.read_int()
        vehicleID = self.connection.read_int()
        toReturn = {"EID": EID,
                    "vehicleID": vehicleID}

        return toReturn

    def handle28(self):
        EID = self.connection.read_int()
        metadata = FIXME
        toReturn = {"EID": EID,
                    "metadata": metadata}

        return toReturn

    def handle29(self):  # TODO Fix this later
        EntityID = self.connection.read_int()
        EffectID = self.connection.read_byte()
        Amplifier = self.connection.read_byte()
        Duration = self.connection.read_short()
        toReturn = {"entityID": EntityID,
                    "effectID": EffectID,
                    "amplifier": Amplifier,
                    "duration": Duration}

        return toReturn

    def handle2A(self):
        EID = self.connection.read_int()
        effectID = self.connection.read_byte()
        toReturn = {"EID": EID,
                    "effectID": effectID}

        return toReturn

    def handle2B(self):
        exp_bar = self.connection.read_float()
        level = self.connection.read_short()
        total_exp = self.connection.read_short()
        toReturn = {"exp_bar": exp_bar,
                    "level": level,
                    "total_exp": total_exp}

        return toReturn

    def handle33(self):  # TODO Fix this bad boy!
        X = self.connection.read_int()
        Z = self.connection.read_int()
        GroundUpContinous = self.connection.read_boolean()
        PrimaryBitMap = self.connection.read_short()
        AddBitMap = self.connection.read_short()
        CompressedSize = self.connection.read_int()
        self.data.readByteArray(CompressedSize)
        #not going to be deflating and using this data until I know how to :3
        toReturn = {"x": X,
                    "z": Z}

        del GroundUpContinous, PrimaryBitMap, AddBitMap  # To make pylint happy

        return toReturn

    def handle34(self):  # TODO Fix this one too!
        ChunkX = self.connection.read_int()
        ChunkZ = self.connection.read_int()
        AffectedBlocks = self.connection.read_short()
        DataSize = self.connection.read_int()
        self.data.readByteArray(DataSize)
        # not going to be using this until I know how to.
        toReturn = {"chunkX": ChunkX,
                    "chunkZ": ChunkZ,
                    "affectedBlocks": AffectedBlocks}

        return toReturn

    def handle35(self):
        x = self.connection.read_int()
        y = self.connection.read_byte()
        z = self.connection.read_int()
        block_type = self.connection.read_short()
        block_metadata = self.connection.read_byte()
        toReturn = {"x": x,
                    "y": y,
                    "z": z,
                    "block_type": block_type,
                    "block_metadata": block_metadata}

        return toReturn

    def handle36(self):
        x = self.connection.read_int()
        y = self.connection.read_short()
        z = self.connection.read_int()
        byte1 = self.connection.read_byte()
        byte2 = self.connection.read_byte()
        blockID = self.connection.read_short()

        toReturn = {"x": x,
                    "y": y,
                    "z": z,
                    "byte1": byte1,
                    "byte2": byte2,
                    "blockID": blockID}

        return toReturn

    def handle37(self):
        EID = self.connection.read_int()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        stage = self.connection.read_byte()

        toReturn = {"EID": EID,
                    "x": x,
                    "y": y,
                    "z": z,
                    "stage": stage}

        return toReturn

    def handle38(self):  # TODO Fix this.
        #short - number of chunks
        ChunkCount = self.connection.read_short()

        #int - chunk data length
        ChunkDataLength = self.connection.read_int()
        self.data.readByteArray(ChunkDataLength)
        # just gonna ignore this for now

        #metadata - ignoring this
        for i in range(ChunkCount):
            self.data.read(12)

        toReturn = {"chunkCount": ChunkCount}

        return toReturn

    def handle3C(self):
        x = self.connection.read_double()
        y = self.connection.read_double()
        z = self.connection.read_double()
        radius = self.connection.read_float()
        record_count = self.connection.read_int()
        affected_blocks = []
        for i in range(RecordCount * 3):
            x = self.connection.read_byte()
            y = self.connection.read_byte()
            z = self.connection.read_byte()
            affected_blocks.append({'x': x, 'y': y, 'z': z})

        velocityX = self.connection.read_float()
        velocityY = self.connection.read_float()
        velocityZ = self.connection.read_float()

        toReturn = {"x": x,
                    "y": y,
                    "z": z,
                    "radius": radius,
                    "affected_blocks": affected_blocks,
                    "velocityX": velocityX,
                    "velocityY": velocityY,
                    "velocityZ": velocityZ}

        return toReturn

    def handle3D(self):  # TODO See data field on wiki
        effectID = self.connection.read_int()
        x = self.connection.read_int()
        y = self.connection.read_byte()
        z = self.connection.read_int()
        data = self.connection.read_int()
        no_volume_decrease = self.connection.read_boolean()
        toReturn = {"effectID": effectID,
                    "x": x,
                    "y": y,
                    "z": z,
                    "data": data,
                    "no_volume_decrease": no_volume_decrease}

        return toReturn

    def handle3E(self):
        sound = self.connection.read_string()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        volume = self.connection.read_float()
        pitch = self.connection.read_byte()
        toReturn = {"sound": sound,
                    "x": x,
                    "y": y,
                    "z": z,
                    "volume": volume,
                    "pitch": pitch}

        return toReturn

    def handle3F(self):
        particle = self.connection.read_string()
        x = self.connection.read_float()
        y = self.connection.read_float()
        z = self.connection.read_float()
        offsetX = self.connection.read_float()
        offsetY = self.connection.read_float()
        offsetZ = self.connection.read_float()
        speed = self.connection.read_float()
        amount = self.connection.read_int()

        toReturn = {"particle": particle,
                    "x": x,
                    "y": y,
                    "z": z,
                    "offsetX": offsetX,
                    "offsetY": offsetY,
                    "offsetZ": offsetZ,
                    "speed": speed,
                    "amount": amount}

        return toReturn

    def handle46(self):
        reason = self.connection.read_byte()
        game_mode = self.connection.read_byte()
        toReturn = {"reason": reason,
                    "game_mode": game_mode}

        return toReturn

    def handle47(self):
        EID = self.connection.read_int()
        type = self.connection.read_byte()
        x = self.connection.read_int()
        y = self.connection.read_int()
        z = self.connection.read_int()
        toReturn = {"EID": EID,
                    "type": type,
                    "x": x,
                    "y": y,
                    "z": z}

        return toReturn

    def handle64(self):
        windowID = self.connection.read_byte()
        inventory_type = self.connection.read_byte()
        window_title = self.connection.read_string()
        slots = self.connection.read_byte()
        use_window_title = self.connection.read_boolean()
        toReturn = {"windowID": windowID,
                    "inventory_type": inventory_type,
                    "window_title": window_title,
                    "slots": slots,
                    "use_window_title": use_window_title}

        return toReturn

    def handle65(self):
        windowID = self.connection.read_byte()

        toReturn = {"windowID": windowID}

        return toReturn

    def handle67(self):  # TODO Fix this
        windowID = self.connection.read_byte()
        slot = self.connection.read_short()
        SlotData = FIXME
        toReturn = {"windowID": WindowID,
                    "slot": Slot,
                    "slotData": SlotData}

        return toReturn

    def handle68(self):  # TODO Fix this
        WindowID = self.connection.read_byte()
        Count = self.connection.read_short()
        Slots = []
        for i in range(Count):
            SlotData = FIXME
            Slots.append(SlotData)
        toReturn = {"windowID": WindowID,
                    "count": Count,
                    "slots": Slots}

        return toReturn

    def handle69(self):
        windowID = self.connection.read_byte()
        property = self.connection.read_short()
        value = self.connection.read_short()
        toReturn = {"windowID": windowID,
                    "property": property,
                    "value": value}

        return toReturn

    def handle6A(self):
        windowID = self.connection.read_byte()
        action_number = self.connection.read_short()
        accepted = self.connection.read_boolean()
        toReturn = {"windowID": windowID,
                    "action_number": action_number,
                    "accepted": accepted}

        return toReturn

    def handle6B(self):  # TODO asd
        Slot = self.connection.read_short()
        ClickedItem = FIXME
        toReturn = {"slot": Slot,
                    "clickedItem": ClickedItem}

        return toReturn

    def handle82(self):
        x = self.connection.read_int()
        y = self.connection.read_short()
        z = self.connection.read_int()
        line1 = self.connection.read_string()
        line2 = self.connection.read_string()
        line3 = self.connection.read_string()
        line4 = self.connection.read_string()
        toReturn = {"x": x,
                    "y": y,
                    "z": z,
                    "line1": line1,
                    "line2": line2,
                    "line3": line3,
                    "line4": line4}

        return toReturn

    def handle83(self):
        item_type = self.connection.read_short()
        itemID = self.connection.read_short()
        text_length = self.connection.read_short()
        text = self.data.readByteArray(TextLength)
        #TODO Decode text?
        toReturn = {"item_type": item_type,
                    "itemID": itemID,
                    "text": text}

        return toReturn


    def handle84(self):
        # TODO NBTData, no idea what it is used for
        # Might be fun to explore this and document it on wiki.vg
        X = self.connection.read_int()
        Y = self.connection.read_short()
        Z = self.connection.read_int()
        Action = self.connection.read_byte()
        DataLength = self.connection.read_short()
        if (DataLength != -1):
            NBTData = struct.unpack(str(DataLength) + "s",
                                    self.data.read(DataLength))[0]
            toReturn = {"x": X,
                        "y": Y,
                        "z": Z,
                        "action": Action,
                        "nbtData": NBTData}

            return toReturn

        toReturn = {"x": X,
                    "y": Y,
                    "z": Z,
                    "action": Action}

        return toReturn

    def handleC8(self):
        statID = self.connection.read_int()
        amount = self.connection.read_byte()
        toReturn = {"statID": statID,
                    "amount": amount}

        return toReturn

    def handleC9(self):
        player_name = self.connection.read_string()
        online = self.connection.read_boolean()
        ping = self.connection.read_short()
        toReturn = {"player_name": player_name,
                    "online": online,
                    "ping": ping}

        return toReturn

    def handleCA(self):
        flags = self.connection.read_byte()  # TODO Decode flags?
        fly_speed = self.connection.read_byte()
        walk_speed = self.connection.read_byte()

        toReturn = {"flags": flags,
                    "fly_speed": fly_speed,
                    "walk_speed": walk_speed}

        return toReturn

    def handleCB(self):
        # TODO Split text field
        # See wiki.vg
        text = self.connection.read_string()
        toReturn = {"text": text}

        return toReturn

    def handleCE(self):
        name = self.connection.read_string()
        value = self.connection.read_string()
        action = self.connection.read_byte()  # TODO Decode action

        toReturn = {"name": name,
                    "value": value,
                    "action": action}

        return toReturn

    def handleCF(self):
        item_name = self.connection.read_string()
        action = self.connection.read_byte()  # TODO Decode action
        score_name = self.connection.read_string()
        value = self.connection.read_int()

        toReturn = {"item_name": item_name,
                    "action": action,
                    "score_name": score_name,
                    "value": value}

        return toReturn

    def handleD0(self):
        position = self.connection.read_byte()  # TODO Decode position
        name = self.connection.read_string()

        toReturn = {"position": position,
                    "name": name}

        return toReturn

    def handleD1(self):  # TODO FIX LATER
        team_name = self.connection.read_string()
        mode = self.connection.read_byte()  # TODO Decode mode
        team_display_name = self.connection.read_string()
        team_prefix = self.connection.read_string()
        team_suffix = self.connection.read_string()
        friendly_fire = self.connection.read_boolean

    def handleFA(self):  # TODO FIX LATER
        channel = self.connection.read_string()
        length = self.connection.read_short()
        message = self.data.readByteArray(length)
        toReturn = {"channel": Channel,
                    "message": message}

        return toReturn

    def handleFC(self):
        secret = self.connection.read_bytearray()
        token = self.connection.read_bytearray()

        toReturn = {"secret": secret,
                    "token": token}

        return toReturn

    def handleFD(self):
        serverID = self.connection.read_string()
        pubkey = self.connection.read_bytearray()
        token = self.connection.read_bytearray()

        toReturn = {"serverID": serverID,
                    "pubkey": pubkey,
                    "token": token}

        return toReturn

    def handleFF(self):
        reason = self.connection.read_string()

        toReturn = {"reason": reason}

        return toReturn
