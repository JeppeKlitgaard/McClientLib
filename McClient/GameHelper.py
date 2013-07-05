# Helper functions for certain in-game actions.
from networking import PacketSenderManager
import time


def breakBlock(seconds, socket, x, y, z, face):
    PacketSenderManager.send0E(socket, 0, x, y, z, face)
    time.sleep(seconds)
    PacketSenderManager.send0E(socket, 2, x, y, z, face)


def placeBlock(socket, x, y, z, direction=0, held=-1, cpx=0, cpy=0, cpz=0):
    PacketSenderManager.send0F(socket, x, y, z, direction=direction, held=held,
                               cpx=cpx, cpy=cpy, cpz=cpz)


def dropItem(socket):
    PacketSenderManager.send0E(socket, 4, 0, 0, 0, 0)


def selectItem(socket, slot):
    PacketSenderManager.send10(socket, slot)


def swingArm(socket, eid):
    PacketSenderManager.send12(socket, eid, animation=1)


def sendChat(socket, message):
    PacketSenderManager.send03(socket, message)
