__author__ = 'Geolffrey Mena <gmjun2000@gmail.com>'

from twisted.internet import protocol, reactor

PORT = 9000


class Client(protocol.ClientFactory):
    """
    SClient Creator
    """

    def __init__(self):
        self.connection = None

    def startedConnecting(self, connector):
        print("Conected to " + connector.getDestination())
        self.connection = connector

    def clientConnectionFailed(self, connector, reason):
        return False

    def clientConnectionLost(self, connector, reason):
        return False


class ClientBox(reactor):
    def __init__(self):
        self.client = Client()
        self.connectTCP('127.0.0.1', PORT, self.client)
        self.run()

    def close(self):
        self.client.connection.stopConnecting()

