from twisted.internet import reactor
from twisted.internet import protocol


class TCPProtocol(protocol.Protocol):

    def __init__(self):

        pass

    def connectionMade(self):
        print "New Connection"

    def connectionLost(self, reason=protocol.connectionDone):
        print 'Connection Lost: %s' % reason
        try:
            print 'Closing connection'
            self.factory.clients.remove(self)
        except ValueError:
            print 'Client not found'

    def dataReceived(self, data):
        if 'ECHO' in data:
            msg = data.split(':')[1]
            print "New ECHO: " + data
            self.transport.write(msg)

        else:
            print "New Message: " + data


def run():
    factory = protocol.Factory()
    factory.protocol = TCPProtocol
    factory.clients = []
    reactor.listenTCP(8123, factory)
    reactor.run()

if __name__ == "__main__":
    run()