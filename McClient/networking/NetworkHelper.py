from Encryption import generate_secret, get_cipher
from Exceptions import NetworkError
from Utils import generate_serverID


class NetworkHelper(object):
    def respondFD(self, serverID, pubkey, token):
        self.secret = generate_secret()
        cipher = get_cipher(pubkey)

        serverID = generate_serverID(serverID, self.secret, pubkey)
        self.session.joinserver(serverID)

        secret = cipher.encrypt(self.secret)
        token = cipher.encrypt(token)

        self.sender.send_encryption_key_response(secret, token)

    def respondFC(self, secret, token):
        if secret or token:
            raise NetworkError("Server didn't respond with empty FC.")
        self.socket.encrypt(self.secret)
        self.sender.send_client_status(0)

    def respond00(self, KID):
        self.sender.send_keepalive(KID)
