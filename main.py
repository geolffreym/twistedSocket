__author__ = 'gmena'

from twisted.internet import protocol, reactor
from twisted.internet.error import ConnectionDone

PORT = 9000


class Socket(protocol.Protocol):
    """Subclass Socket Connection"""

    def __init__(self, users):
        self.myPeer = None
        self.myName = None
        self.myClients = users

    def dataReceived(self, data):
        self.handleRequest(self, data)

    def connectionMade(self):
        self.myPeer = self.transport.getPeer()

    def connectionLost(self, reason=ConnectionDone):
        if self.getClient(self.myName):
            del self.myClients[self.myName]

    def isMessage(self, request):
        my_request = request.split(':')
        if my_request[0] and my_request[1]:
            if my_request[0] != 'auth':
                return {
                    'recipient': my_request[0],
                    'message': my_request[1]
                }

        return False

    def isAuth(self, request):
        my_request = request.split(':')
        if my_request[0]:
            if my_request[0] == 'auth':
                if my_request[1]:
                    return {
                        'action': my_request[0],
                        'name': my_request[1]
                    }

        return False

    def handleRequest(self, tmp_client_connection, request):
        """"
        Handle Request
        authenticate-> action:user
        send-> recipient:message
        """
        if not self.myName:
            new_client = self.isAuth(request)
            self.createClient(tmp_client_connection, new_client)
        else:
            new_message = self.isMessage(request)
            if new_message:
                self.handleMessage(new_message)

    def handleMessage(self, message):
        recipient = self.getClient(message.recipient)
        if recipient:
            recipient.write(message.message)
        else:
            print ('The recipient not exist')

    def getClient(self, name):
        if self.myClients[name]:
            return self.myClients[name]
        return False

    def createClient(self, client, client_data):
        self.myName = client_data.name
        self.myClients[self.myName] = client.transport


class SocketFactory(protocol.Factory):
    """Socket Factory"""

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Socket(self.users)


reactor.listenTCP(PORT, SocketFactory())
reactor.run()