from twisted.internet import reactor
from twisted.internet import protocol

TCP_PORT = 8123


class TCPProtocol(protocol.Protocol):


    def __init__(self):
        self.ack_count = 0
        pass

    def connectionMade(self):
        print("New Connection")

    def connectionLost(self, reason=protocol.connectionDone):
        print(f'Connection Lost: {reason}')
        try:
            print('Closing connection')
            self.factory.clients.remove(self)
        except ValueError:
            print('Client not found')

    def dataReceived(self, data):
        print(f"Data received: {data}")
        self.transport.write(data=f"ACK {self.ack_count}".encode('utf-8'))
        self.ack_count += 1

def run():
    factory = protocol.Factory()
    factory.protocol = TCPProtocol
    factory.clients = []
    reactor.listenTCP(TCP_PORT, factory)
    print(f"Listening for connections on port {TCP_PORT}")
    reactor.run()
    print(f"Reactor closed")


if __name__ == "__main__":
    run()
