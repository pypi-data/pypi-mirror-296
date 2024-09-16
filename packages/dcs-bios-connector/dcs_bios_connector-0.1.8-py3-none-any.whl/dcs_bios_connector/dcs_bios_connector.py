

from pyee import EventEmitter
from .control_parser import ControlParser
from .udp_listener import UdpListener


class DcsBiosConnector(EventEmitter):

    def __init__(self):
        super().__init__()
        self.updListener = UdpListener()
        self.control_parser = ControlParser()
    
    def connect(self):
        self.updListener.start()
    
    def send(self):
        print("not implemented yet")
