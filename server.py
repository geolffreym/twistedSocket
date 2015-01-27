__author__ = 'Geolffrey Mena <gmjun2000@gmail.com>'

from twisted.internet import protocol, reactor
from twisted.internet.error import ConnectionDone

PORT = 9000


class Socket(protocol.Protocol):
    """
    Subclass Socket Connection
    http://twistedmatrix.com/documents/current/api/twisted.internet.protocol.Protocol.html
    """

    def __init__(self, users):
        self.myPeer = None
        self.myName = None
        self.myClients = users

    def dataReceived(self, data):
        """Handle data received"""
        self.handleRequest(self, data)

    def connectionMade(self):
        self.myPeer = self.transport.getPeer()
        print('Connection attemp from: ' + self.myPeer)


    def connectionLost(self, reason=ConnectionDone):
        if self.getClient(self.myName):
            del self.myClients[self.myName]

    def isCommand(self, request):
        my_request = request.split(':')
        if my_request[0] and my_request[1]:
            return {
                'param1': my_request[0],
                'param2': my_request[1]
            }
        return False

    def isMessage(self, request):
        my_request = self.isCommand(request)

        if my_request:
            if my_request.get('param1') != 'auth':
                return {
                    'recipient': my_request.get('param1'),
                    'message': my_request.get('param2')
                }

        return False

    def isAuth(self, request):
        my_request = self.isCommand(request)
        if my_request:
            if my_request.get('param1') == 'auth':
                return {
                    'action': my_request.get('param1'),
                    'name': my_request.get('param2')
                }

        return False

    def handleRequest(self, tmp_client_connection, request):
        """"
        Handle Request
        authenticate-> action:user
        send-> recipient:message
        """
        new_client = self.isAuth(request)
        if new_client:
            self.createClient(tmp_client_connection, new_client)
        else:
            new_message = self.isMessage(request)
            if new_message:
                self.handleMessage(new_message)
            else:
                print('Unknown Action')

    def handleMessage(self, message):
        recipient = self.getClient(message.get('recipient', None))
        if recipient:
            new_message = message.get('message', None)
            if new_message is not None:
                recipient.write(new_message)
        else:
            print ('The recipient not exist')

    def getClient(self, name):
        if name is not None:
            if self.myClients[name]:
                return self.myClients[name]
        return False

    def createClient(self, client, client_data):
        client_name = client_data.get('name', None)
        if client_name is not None:
            if not self.myName:
                print('New Client created: ' + self.myName)
                self.myName = client_name
                self.myClients[self.myName] = client.transport


class SocketFactory(protocol.Factory):
    """
    Socket Factory
    http://twistedmatrix.com/documents/current/api/twisted.internet.protocol.Factory.html
    """

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Socket(self.users)


print("Listening on port " + str(PORT) + "...")
reactor.listenTCP(PORT, SocketFactory())
reactor.run()