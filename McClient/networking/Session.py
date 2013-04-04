from Exceptions import SessionError, SessionBadLogin, SessionVersionError
import urllib
import urllib2


class BaseSession(object):
    game_version = None
    username = None
    sessionID = None
    UID = None
    online = False

    def connect(self, username, password):
        raise NotImplementedError()

    def joinserver(self, serverID):
        raise NotImplementedError()


class Session(BaseSession):
    """Session object for connecting to online server."""
    __LOGIN_URL = "https://login.minecraft.net"
    __LOGIN_HEADER = {"Content-Type": "application/x-www-form-urlencoded"}
    __JOIN_URL = "http://session.minecraft.net/game/joinserver.jsp"
    VERSION = 13

    def connect(self, username, password):
        """Connects minecraft.net and gets a session id."""
        data = urllib.urlencode({"user": username,
                                 "password": password,
                                 "version": self.VERSION})
        req = urllib2.Request(self.__LOGIN_URL, data, self.__LOGIN_HEADER)
        opener = urllib2.build_opener()
        try:
            response = opener.open(req, None, 10).read()
        except urllib2.URLError:
            raise SessionError("Unable to connect to login server.")

        if response.lower() == "bad login":
            raise SessionBadLogin("Wrong username/password combination.")

        if response.lower() in ("old version", "bad response"):
            raise SessionVersionError("Client version deprecated.")

        if response.lower() == "account migrated, use e-mail":
            raise SessionBadLogin("Account migrated, use e-mail")

        response = response.split(":")

        self.online = True

        self.game_version = response[0]
        # field #1 is deprecated, always!
        self.username = response[2]
        self.sessionID = response[3]
        self.UID = response[4]

    def joinserver(self, serverID):
        url = self.__JOIN_URL + "?user=%s&sessionId=%s&serverId=%s" \
            % (self.username, self.sessionID, serverID)

        response = urllib2.urlopen(url).read()

        if response != "OK":
            raise SessionError("Authenticating with Minecraft.net failed, " +
                               "response was: %s" % response)

        return True


class OfflineSession(BaseSession):
    """Session object for connecting to offline servers."""
    def connect(self, username, password):
        """Since this is offline mode, we don't need the password."""
        self.username = username
        self.sessionID = "-"

    def joinserver(self, serverID):
        """Since this is offline mode, we don't need the serverID."""
        pass
