__author__ = 'Geolffrey Mena <gmjun2000@gmail.com>'

from twisted.internet import protocol, reactor

PORT = 9000


class Client(protocol.Protocol):
    def __init__(self, connection):
        self.myConnection = connection
        self.myPeer = connection.getDestination()

    def dataReceived(self, data):
        """Handle data received"""
        print(data)


class ClientFactory(protocol.ClientFactory):
    """
    SClient Creator
    """

    def __init__(self):
        self.connection = None
        self.host = None

    def startedConnecting(self, connector):
        self.connection = connector
        self.host = str(connector.getDestination().host)
        print "Start Connecting to ", self.host

    def buildProtocol(self, addr):
        print 'Connected to ', self.host
        return Client(self.connection)

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        print 'Reconnecting..'
        connector.connect()


reactor.connectTCP('127.0.0.1', PORT, ClientFactory())
reactor.run()