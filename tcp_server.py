from twisted.internet import reactor
from twisted.internet import protocol

from PIL import Image
import numpy as np

# This will take a byte array with the structure [UInt8 MSB0, UInt8 LSB0, UInt8 MSB1, UInt8 LSB1, ....
# for all 16bit 5/6/5 RRRRRGGG GGGBBBBB pixels, 6400 in total for the 80x80 array. Extract the colors,
# write them into an 80x80 image
def createImageFromByteArray(data):
    newIm = Image.new('RGB', (80, 80), (0, 0, 0))
    pixels = newIm.load()
    x = 0
    y = 0
    print "Data Size: " + str(len(data))
    for i in range(0, 12800, 2):
        #print "Data: " + hex(data[i]) + " " + hex(data[i+1])
        color16 = (np.uint16(data[i]) << 8) | np.uint16(data[i + 1])
        r = np.uint8(color16 >> 8) & 0xF8
        g = np.uint8(color16 >> 3) & 0xFC
        b = np.uint8(color16 << 3) & 0xF8
        pixels[x, y] = (r, g, b)
        x += 1
        if (x >= 80):
            y += 1
            x = 0

    newIm.show()

class TCPProtocol(protocol.Protocol):

    imageArray = []

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
            buff = bytearray(data)
            print "Received " + str(len(buff)) + " bytes"
            self.imageArray.extend(buff)
            if len(self.imageArray) == 12800:
                print "Creating Image"
                createImageFromByteArray(self.imageArray)
                self.imageArray = []
            else:
                print "Array Length: " + str(len(self.imageArray))

def run():
    factory = protocol.Factory()
    factory.protocol = TCPProtocol
    factory.clients = []
    print "TCP Server Started"
    reactor.listenTCP(8123, factory)
    reactor.run()


if __name__ == "__main__":
    run()