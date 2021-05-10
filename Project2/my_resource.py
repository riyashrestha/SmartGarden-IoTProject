import time
import Adafruit_DHT
DHT_SENSOR =Adafruit_DHT.DHT11
DHT_PIN = 17

from coapthon import defines
from coapthon.resources.resource import Resource

class MyDHT11Resource(Resource):
    def __init__(self, name="MyDHT11Resource", coap_server=None):
        super(MyDHT11Resource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "My DHT11 Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        self.humidity = 0
        self.temperature = 0
        
    def readings(self):
        self.humidity, self.temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    def render_GET(self, request):
        self.readings()
        self.payload = "Temp={:.1f}C Humidity={:.1f}%".format(self.temperature, self.humidity)
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self

    def render_POST(self, request):
        res = self.init_resource(request, MyDHT11Resource())
        return res

    def render_DELETE(self, request):
        return True
    