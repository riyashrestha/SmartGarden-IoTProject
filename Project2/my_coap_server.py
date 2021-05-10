from coapthon.server.coap import CoAP
from my_resource import MyDHT11Resource



class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('MyDHT11/', MyDHT11Resource())

def main():
    server = CoAPServer("192.168.0.22", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print ("Server Shutdown")
        server.close()
        print ("Exiting...")

if __name__ == '__main__':
    main()