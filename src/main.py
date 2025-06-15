from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.config import Config
import obd
from utils.obd_manager import OBDManager
from gui.screens import Dashboard

# Set the window size
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', 800)    # pi screen dimensions: 800x480
Config.set('graphics', 'height', 440)

# Designate the .kv file
kv = Builder.load_file("gui/kv/main.kv")

# Define sensor configs for each screen
SENSOR_CONFIGS = {
    'home': {
        'names': ["RPM", "Speed", "Engine Temp", "Fuel Level", "Battery Volts", "Engine Load"],
        'units': [" RPM", " km/h", "°C", "%", " V", " %"],
        'obd_commands': [
            obd.commands.RPM,
            obd.commands.SPEED,
            obd.commands.COOLANT_TEMP,
            obd.commands.FUEL_LEVEL,
            obd.commands.CONTROL_MODULE_VOLTAGE, # ECU voltage, often very close to battery
            obd.commands.ENGINE_LOAD
        ]
    },
    'fuel': {
        'names': ["Fuel Level", "Fuel Pressure", "Fuel Type", "Fuel Rail Pres (Rel)", "Short Term Fuel Trim (B1)", "Long Term Fuel Trim (B1)"],
        'units': [" %", " kPa", "", " kPa", " %", " %"],
        'obd_commands': [
            obd.commands.FUEL_LEVEL,
            obd.commands.FUEL_PRESSURE,
            obd.commands.FUEL_TYPE, # May return a number, could map to string
            obd.commands.FUEL_RAIL_PRESSURE_ABS,
            obd.commands.SHORT_FUEL_TRIM_1,
            obd.commands.LONG_FUEL_TRIM_1
        ]
    },
    'battery': {
        'names': ["Control Module Volts", "Fuel Rail Volts", "Run Time", "Distance Traveled", "Ambient Air Temp", "Engine RPM"], # Reusing some for demonstration
        'units': [" V", " V", " s", " km", "°C", " RPM"],
        'obd_commands': [
            obd.commands.CONTROL_MODULE_VOLTAGE,
            obd.commands.FUEL_RAIL_PRESSURE_ABS, # Using pressure for voltage (example) - can swap if better PID exists
            obd.commands.RUN_TIME,
            obd.commands.DISTANCE_SINCE_DTC_CLEAR,
            obd.commands.AMBIANT_AIR_TEMP,
            obd.commands.RPM
        ]
    },
    'temp': {
        'names': ["Engine Coolant Temp", "Intake Air Temp", "Ambient Air Temp", "Catalyst Temp (B1S1)", "MAF Sensor Temp (Calc)", "Throttle Position (Temp-related)"],
        'units': ["°C", "°C", "°C", "°C", "°C", " %"],
        'obd_commands': [
            obd.commands.COOLANT_TEMP,
            obd.commands.INTAKE_TEMP,
            obd.commands.AMBIANT_AIR_TEMP,
            obd.commands.CATALYST_TEMP_B1S1,
            None, # MAF Temp not a common direct PID, can be derived
            obd.commands.THROTTLE_POS # Indirectly related to engine temp via air flow
        ]
    },
    'warning': {
        'names': ["DTC Count", "Time Since DTC Cleared", "Fuel System Status", "O2 Sensors Status", "Status Since DTC Cleared", "Evap System Vapor Pressure"],
        'units': ["", "", "", "", "", " kPa"],
        'obd_commands': [
            obd.commands.GET_DTC, # This returns a list of DTCs, you might want to count them or show first few
            obd.commands.TIME_SINCE_DTC_CLEARED,
            obd.commands.FUEL_STATUS,
            obd.commands.O2_SENSORS, # Bitmask of supported O2 sensors
            obd.commands.STATUS,
            obd.commands.EVAP_VAPOR_PRESSURE # Useful for evap system health
        ]
    },
    'engine': {
        'names': ["Manifold Abs. Pressure", "Mass Air Flow", "Throttle Position", "Timing Advance", "Engine Load", "Air/Fuel Ratio (Commanded)"],
        'units': [" kPa", " g/s", " %", "°", " %", ""],
        'obd_commands': [
            obd.commands.INTAKE_PRESSURE,
            obd.commands.MAF,
            obd.commands.THROTTLE_POS,
            obd.commands.TIMING_ADVANCE,
            obd.commands.ENGINE_LOAD,
            obd.commands.COMMANDED_EQUIV_RATIO # Commanded A/F ratio
        ]
    }
}

class RootWidget(BoxLayout):
    # This class holds the ScreenManager and the sidebar with buttons.
    
    screen_manager = ObjectProperty(None)    # reference to ScreenManager instance
    obd_manager = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obd_manager = OBDManager()
        
        for screen_name, config in SENSOR_CONFIGS.items():
            screen_instance = Dashboard(obd_manager_instance=self.obd_manager, name=screen_name)
            self.ids.screen_manager_id.add_widget(screen_instance)
            # Set initial data for each screen right after adding it
            screen_instance.set_sensor_data(
                config['names'],
                config['units'],
                config['obd_commands']
            )
            
        # Set the initial screen (e.g., 'home')
        self.ids.screen_manager_id.current = 'home'
                
        
    def switch_screen(self, screen_name):
        # This method is called from the sidebar btns in main.kv
        if self.screen_manager:
            self.screen_manager.current = screen_name
            self.screen_manager.transition = NoTransition()
            print(f"Switched to screen: {screen_name}")
    
            # get the new active screen instance
            active_screen = self.screen_manager.get_screen(screen_name)
   
            # check if active screen has set_sensor_data method
            if hasattr(active_screen, 'set_sensor_data'):
                config = SENSOR_CONFIGS.get(screen_name)
                if config:
                    active_screen.set_sensor_data(
                        config['names'], 
                        config['units'],
                        config['obd_commands']
                        )
                else:
                    print(f"No sensor configuration found for screen: {screen_name}")
            else:
                print(f"Screen '{screen_name}' does not have a 'set_sensor_data' method.")

class MainApp(App):
    def build(self):
        return RootWidget()
    
    def on_stop(self):
        if self.root and hasattr(self.root, 'obd_manager') and self.root.obd_manager:
            self.root.obd_manager.close()

if __name__ == '__main__':
    MainApp().run()
