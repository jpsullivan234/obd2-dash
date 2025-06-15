import obd

class OBDManager:
    # Manages the OBD-II connection and data queries, as well as all interactions
    # with the python-obd lib
    
    def __init__(self, port='/dev/ttyUSB0'):
        self.connection = None
        self._port = port
        self.connect()
        
    