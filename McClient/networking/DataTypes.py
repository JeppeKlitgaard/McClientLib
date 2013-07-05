import struct
from io import BytesIO
from pynbt import NBTFile
from McClient.networking.Utils import hex2str


data_types = {
    "ubyte": 'B',
    "byte": 'b',
    "bool": '?',
    "short": 'h',
    "ushort": 'H',
    "float": 'f',
    "int": 'i',
    "uint": 'I',
    "double": 'd',
    "long": 'q',
}


class TypeReader(object):
    """This class reads the different data types.
    Does nothing on it's own, just another cog in the machine!"""
    @staticmethod
    def _unpack(data_type, data):
        fmt = "!" + data_types[data_type]
        return struct.unpack(fmt, data)[0]

    def read_id(self):
        pid = self.read(1)
        pid = hex2str(pid)
        return pid

    def read_int(self):
        data = self._unpack("int", self.read(4))
        return data

    def read_short(self):
        data = self._unpack("short", self.read(2))
        return data

    def read_ushort(self):
        data = self._unpack("ushort", self.read(2))
        return data

    def read_string(self):
        length = self.read_short() * 2
        data = unicode(self.read(length), "utf-16be")
        return data

    def read_byte(self):
        data = self._unpack("byte", self.read(1))
        return data

    def read_ubyte(self):
        data = self._unpack("ubyte", self.read(1))
        return data

    def read_long(self):
        data = self._unpack("long", self.read(8))
        return data

    def read_boolean(self):
        data = self._unpack("bool", self.read(1))
        return data

    def read_float(self):
        data = self._unpack("float", self.read(4))
        return data

    def read_double(self):
        data = self._unpack("double", self.read(8))
        return data

    def read_bytearray(self, length=None):
        if not length:
            length = self.read_short()
        data = struct.unpack("!" + str(length) + "s", self.read(length))[0]
        return data

    def read_slot(self):
        slot = Slot()
        slot.blockID = self.read_short()
        if slot.blockID != -1:
            slot.count = self.read_byte()
            slot.damage = self.read_short()

            data_len = self.read_short()
            if data_len != -1:
                byte_array = self.read_bytearray(length=data_len)

                slot.data = NBTFile(BytesIO(byte_array),
                                    compression=NBTFile.Compression.GZIP)

        return slot

    def read_metadata(self):
        metadata = {}
        byte = self.read_ubyte()
        while byte != 127:
            index = byte & 0x1F  # Lower 5 bits
            ty = byte >> 5  # Upper 3 bits

            if ty == 0:
                value = self.read_byte()
            if ty == 1:
                value = self.read_short()
            if ty == 2:
                value = self.read_int()
            if ty == 3:
                value = self.read_float()
            if ty == 4:
                value = self.read_string()
            if ty == 5:
                value = self.read_slot()
            if ty == 6:
                value = []
                for i in range(3):
                    value.append(self.read_int())
            metadata[index] = (ty, value)
            byte = self.read_ubyte()

        return metadata

    def read_nbtdata(self, compressed=True):
        data = None

        length = self.read_short()
        if length != -1:
            byte_array = self.read_bytearray(length=length)
            if compressed:
                data = NBTFile(BytesIO(byte_array),
                               compression=NBTFile.Compression.GZIP)
            else:
                data = NBTFile(BytesIO(byte_array))

        return data

    def read_object_data(self):
        data = {"data": None,
                "speedX": None,
                "speedY": None,
                "speedZ": None}

        data["data"] = self.read_int()
        if data["data"] > 0:
            data["speedX"] = self.read_short()
            data["speedY"] = self.read_short()
            data["speedZ"] = self.read_short()

        return data


class TypeWriter(object):
    @staticmethod
    def _pack(data_type, data):
        fmt = "!" + data_types[data_type]
        return struct.pack(fmt, data)

    def write_id(self, pid):
        self.write(pid)

    def write_int(self, data):
        self.write(self._pack("int", data))

    def write_short(self, data):
        self.write(self._pack("short", data))

    def write_ushort(self, data):
        self.write(self._pack("ushort", data))

    def write_string(self, data):
        self.write_short(len(data))
        self.write(data.encode("utf-16be"))

    def write_byte(self, data):
        self.write(self._pack("byte", data))

    def write_ubyte(self, data):
        self.write(self._pack("ubyte", data))

    def write_long(self, data):
        self.write(self._pack("long", data))

    def write_boolean(self, data):
        self.write(self._pack("bool", data))

    def write_float(self, data):
        self.write(self._pack("float", data))

    def write_double(self, data):
        self.write(self._pack("double", data))

    def write_bytearray(self, data):
        self.write_short(len(data))
        self.write(struct.pack("!" + str(len(data)) + "s", data))


class Slot(object):
    def __init__(self, blockID=-1, count=0, damage=None, data=None):
        self.blockID = blockID
        self.count = count
        self.damage = damage
        self.data = data

    def __repr__(self):
        return "<Slot> ID: %s, count: %s, damage: %s, #%s#" % (self.blockID,
                                                               self.count,
                                                               self.damage,
                                                               self.data)

####
#data_types = {
#    "ubyte":  ('B', 1),
#    "byte":   ('b', 1),
#    "bool":   ('?', 1),
#    "short":  ('h', 2),
#    "ushort": ('H', 2),
#    "float":  ('f', 4),
#    "int":    ('i', 4),
#    "uint":   ('I', 4),
#    "double": ('d', 8),
#    "long":   ('q', 8)
#}
#
#
#def unpack(buff, data_type):
#    """Unpacks a data type."""
#    if data_type in data_types:
#        fmt, length = data_types[data_type][0], data_types[data_type][1]
#        return unpack_real(buff, fmt, length)
#
#    if data_type == "bytearray":
#        size = unpack(buff, "short")
#        return unpack_real(buff, str(size) + "s", size)
#
#    raise TypeError("Failed to unpack datatype: %s" % data_type)
#
#
#def unpack_real(buff, data_type, length):
#    return struct.unpack("!" + data_type, buff.read(length))[0]
#
#
#def pack(data_type, data):
#    """Packs a data type."""
#    if data_type in data_types:
#        fmt = data_types[data_type][0]
#        return pack_real(fmt, data)
#
#    if data_type == "string":
#        toReturn = pack("short", data.__len__())
#        toReturn += data.encode("utf-16be")
#        return toReturn
#
#    if data_type == "bytearray":
#        return pack_real(str(data.__len__() + "s"), data)
#
#    raise TypeError("Failed to unpack datatype: %s" % data_type)
#
#
#def pack_real(data_type, data):
#    return struct.pack("!" + data_type, data)
#
#
### TODO Byte Array
#def readByteArray(file_object, length):
#    return struct.unpack(str(length) + "s", file_object.read(length))[0]
#
#
##def writeByteArray(file_object, data):
##    length = data.__len__()
##    writeShort(file_object, length)
##    file_object.write(struct.pack(str(length) + "s", data))
##
##
##def readEntityMetadata(file_object):
#    metadata = {}
#    byte = readUnsignedByte(file_object)
#    while byte != 127:
#        index = byte & 0x1F  # Lower 5 bits
#        ty = byte >> 5  # Upper 3 bits
#        if ty == 0:
#            val = readByte(file_object)
#        if ty == 1:
#            val = readShort(file_object)
#        if ty == 2:
#            val = readInt(file_object)
#        if ty == 3:
#            val = readFloat(file_object)
#        if ty == 4:
#            val = readString(file_object)
#        if ty == 5:
#            val = {}
#            val["id"] = readShort(file_object)
#            if (val["id"] != -1):
#                val["count"] = readByte(file_object)
#                val["damage"] = readShort(file_object)
#                nbtDataLength = readShort(file_object)
#                if (nbtDataLength != -1):
#                    val["NBT"] = NBTFile(BytesIO(
#                        readByteArray(file_object, nbtDataLength)),
#                        compression=NBTFile.Compression.GZIP)
#        if ty == 6:
#            val = []
#            for i in range(3):
#                val.append(readInt(file_object))
#        metadata[index] = (ty, val)
#        byte = readUnsignedByte(file_object)
#    return metadata
#
#
#def readSlot(file_object):
#    #TODO This needs testing
#    slot = Slot()
#    slot.ID = readShort(file_object)
#    if slot.ID != -1:
#        slot.count = readByte(file_object)
#        slot.damage = readShort(file_object)
#        MetadataLength = readShort(file_object)
#        if MetadataLength != -1:
#            ByteArray = readByteArray(file_object, MetadataLength)
#            NBTData = NBTFile(BytesIO(ByteArray),
#                              compression=NBTFile.Compression.GZIP)
#            for tag in NBTData:
#                if tag == "ench":
#                    for ench in NBTData["ench"]:
#                        enchant = SlotEnchant()
#                        enchant.ID = ench["id"].value
#                        enchant.level = ench["lvl"].value
#
#                        slot.data.ench.append(enchant)
#                elif tag == "title":
#                    slot.data.title = NBTData["title"].value
#                elif tag == "author":
#                    slot.data.author = NBTData["author"].value
#                elif tag == "pages":
#                    for page in NBTData["pages"]:
#                        slot.data.pages.append(page.value)
#                elif tag == "display":
#                    tag = NBTData["display"]
#                    slot.data.display.color = tag["color"].value
#                    slot.data.name = tag["Name"].value
#                    for line in tag["Lore"]:
#                        slot.data.lore.append(line)
#                elif tag == "CustomPotionEffects":
#                    tag = NBTData["CustomPotionEffects"]
#                    for pot in tag:
#                        potion = SlotPotionEffect()
#                        potion.ID = pot["Id"].value
#                        potion.amplifier = pot["Amplifier"].value
#                        potion.duration = pot["Duration"].value
#                        potion.ambient = pot["Ambient"].value
#                        slot.data.potion_effects.append(potion)
#                elif tag == "SkullOwner":
#                    slot.data.skull_owner = NBTData["SkullOwner"]
#                elif tag == "RepairCost":
#                    slot.data.repair_cost = NBTData["RepairCost"]
#                elif tag == "map_is_scaling":
#                    slot.data.map_is_scaling = NBTData["map_is_scaling"]
#                else:
#                    raise TypeError("Got unexpected type while unpacking"
#                                    " Slot Data: %s" % tag)
#
#    return slot
#
#
#def writeSlot(file_object, slot):
#    #TODO Needs testing
#    #Like a lot of testing, this is totally untested! Nothing at all!
#    """Writes a slot into minecraft protocol format (NBT)"""
#    if not slot.ID:
#        writeShort(file_object, -1)  # We have no more data
#
#    else:
#        writeShort(file_object, slot.ID)
#        writeByte(file_object, slot.count)
#        writeShort(file_object, slot.damage)
#        if not slot:  # We have no NBT data.
#            writeShort(file_object, -1)
#
#        else:  # We have NBT data,
#                # now we just gotta serialize it and write it
#            nbt = NBTFile()
#            nbt["ench"] = TAG_List()
#
#            for enchant in slot.ench:
#                nbt["ench"].append(TAG_Compound(TAG_Short(enchant.ID,
#                                                          name="id"),
#                                                TAG_Short(enchant.level,
#                                                          name="lvl")))
#            byte_array = BytesIO()
#            nbt.save(byte_array, compression=NBTFile.Compression.GZIP)
#            writeByteArray(file_object, byte_array.read())
