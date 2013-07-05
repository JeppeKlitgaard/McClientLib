from Crypto.Random import _UserFriendlyRNG
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
import socket
from select import select


def generate_secret():
    """Generates a shared secret."""
    secret = _UserFriendlyRNG.get_random_bytes(16)
    return secret


def get_cipher(key):
    key = RSA.importKey(key)
    c = PKCS1_v1_5.new(key)
    return c


class EncryptedSocket(object):
    def __init__(self, socket, cipher):
        self.socket = socket
        self.cipher = cipher

    def send(self, data):
        self.socket.send(self.cipher.encrypt(data))

    def close(self):
        self.socket.close()

    def fileno(self):
        return self.socket.fileno()


class EncryptedFile(object):
    def __init__(self, fileobject, cipher):
        self.file = fileobject
        self.cipher = cipher

    def read(self, *args, **kwargs):
        data = self.cipher.decrypt(self.file.read(*args, **kwargs))
        return data


class UnencryptedSocket(socket.socket):
    pass


class Socket(object):
    def __init__(self):
        self.unencrypted_socket = UnencryptedSocket(socket.AF_INET,
                                                    socket.SOCK_STREAM)
        self.unencrypted_file = None

        self.encrypted_socket = None
        self.encrypted_file = None

        self.cipher = None
        self.decipher = None

        self.socket = self.unencrypted_socket
        self.file = self.unencrypted_file

    def wait4data(self):
        select([self.socket], [], [])

    def connect(self, host, port=25565):
        self.socket.connect((host, port))
        self.unencrypted_file = self.socket.makefile()
        self.file = self.unencrypted_file

    def encrypt(self, secret):
        """Enables encryption."""
        self.cipher = AES.new(secret, AES.MODE_CFB, IV=secret)
        self.decipher = AES.new(secret, AES.MODE_CFB, IV=secret)

        self.encrypted_socket = EncryptedSocket(self.socket, self.cipher)
        self.encrypted_file = EncryptedFile(self.file, self.decipher)
        self.socket = self.encrypted_socket
        self.file = self.encrypted_file

    def read(self, *args, **kwargs):
        return self.file.read(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self.socket.send(*args, **kwargs)

    def close(self):
        self.socket.close()
