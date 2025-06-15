import obd
import random
class OBDManager:
    # Manages the OBD-II connection and data queries, as well as all interactions
    # with the python-obd lib
    
    def __init__(self, port='/dev/ttyUSB0'):
        self.connection = None
        self._port = port
        self.connect()
        print(f"OBDManager initialized. Connection Status: {self.get_status_text()}")
        
    def connect(self):
        if self.connection and self.connection.is_connected():
            return # its already connected
        try:
            if self._port:
                self.connection = obd.OBD(self._port)
            else:
                self.connection = obd.OBD() # try auto connecting
            print(f"Attempting to connect to OBD: {self.connection.status()}")
        except Exception as e:
            print(f"Error establishing OBD connection: {e}")
            self.connection = None
    
    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()
    
    def get_status_text(self):
        if self.connection:
            return f"OBD Status: {self.connection.status()}"
        return "OBD Status: Not Connected"
    
    def query_data(self, obd_commands_list, units_list):
        """
        Queries the OBD-II adapter for data corresponding to the given commands.
        Args:
            obd_commands_list (list): A list of obd.commands objects (or None) to query.
            units_list (list): A list of unit strings for formatting.
        Returns:
            list: A list of formatted data strings for display.
        """
        if not self.is_connected():
            # If not connected, return N/A for all data
            return self._generate_mock_data(obd_commands_list, units_list)
        
        data = []
        for i, cmd in enumerate(obd_commands_list):
            if cmd is None:
                data.append("N/A")
                continue
            
            try:
                response = self.connection.query(cmd)
                
                if response and not response.is_null():
                    # format the value
                    display_value = f"{response.value.magnitude:.1f}"
                    # append units
                    unit = units_list[i] if i < len(units_list) else ""
                    data.append(f"{display_value}{unit}")
                else:
                    data.append("N/A")	# data is not available
            except Exception as e:
                print(f"Error querying OBD command {cmd.name}: {e}")
                data.append("Error")
        return data
    
    def _generate_mock_data(self, obd_commands_list, units_list):
        """
        Generates mock data based on the command type if OBD is not connected.
        """
        mock_data_values = []
        for i, cmd in enumerate(obd_commands_list):
            name = cmd.name if cmd else "UNKNOWN"
            unit = units_list[i] if i < len(units_list) else ""

            if "RPM" in name:
                mock_data_values.append(f"{random.randint(700, 3000)}{unit}")
            elif "SPEED" in name:
                mock_data_values.append(f"{random.randint(0, 120)}{unit}")
            elif "FUEL_LEVEL" in name or "FUEL_RATE" in name or "FUEL_CONSUMPTION" in name:
                mock_data_values.append(f"{random.randint(10, 90)}{unit}")
            elif "TEMP" in name:
                mock_data_values.append(f"{random.randint(80, 100)}{unit}")
            elif "VOLTAGE" in name:
                mock_data_values.append(f"{random.uniform(12.0, 14.5):.1f}{unit}")
            elif "PRESSURE" in name:
                mock_data_values.append(f"{random.randint(30, 60)}{unit}")
            elif "TRIM" in name:
                mock_data_values.append(f"{random.uniform(-5.0, 5.0):.1f}{unit}")
            elif "LAMBDA" in name:
                mock_data_values.append(f"{random.uniform(0.9, 1.1):.2f}{unit}")
            elif "THROTTLE" in name:
                mock_data_values.append(f"{random.randint(0, 100)}{unit}")
            elif "MAF" in name:
                mock_data_values.append(f"{random.uniform(0.5, 5.0):.2f}{unit}")
            elif "TIMING" in name:
                mock_data_values.append(f"{random.uniform(-10.0, 30.0):.1f}{unit}")
            else:
                mock_data_values.append("N/A")
        return mock_data_values
    
    def close(self):
        # Closes the connection
        
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("OBD Connection Closed")
        self.connection = None