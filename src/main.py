from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 480)

# Import the Screen classes
from gui.screens import HomeScreen

# Designate the .kv file
kv = Builder.load_file("gui/kv/main.kv")

# Define sensor configs for each screen
SENSOR_CONFIGS = {
	'home': {
		'names': ["RPM", "Speed", "Fuel Level", "Engine Temp", "Battery Volts", "Oil Pressure"],
		'units': [" RPM", " km/h", "%", "°C", " V", " PSI"]
	},
	'fuel': {
		'names': ["Fuel Flow", "Fuel Consumed", "Fuel Pressure", "Lambda Value", "Short Term Fuel Trim", "Long Term Fuel Trim"],
		'units': [" L/h", " L", " PSI", "", "%", "%"] # Empty string for units that don't need one
	},
	'battery': {
		'names': ["Battery Volts", "Alternator Volts", "Current Draw", "Charge Rate", "Battery Temp", "Battery Health"],
		'units': [" V", " V", " A", " W", "°C", " %"]
	},
	'temp': {
		'names': ["Engine Temp", "Coolant Temp", "Intake Temp", "Ambient Temp", "Oil Temp", "Exhaust Temp"],
		'units': ["°C", "°C", "°C", "°C", "°C", "°C"]
	},
	'warning': {
		'names': ["Check Engine Light", "Low Oil Pressure", "Low Coolant", "Battery Warning", "Brake Fluid Low", "Tire Pressure Warning"],
		'units': ["", "", "", "", "", ""] # No units for these warnings
	},
	'engine': {
		'names': ["Boost Pressure", "Intake Air Flow", "Timing Advance", "Knock Retard", "Engine Load", "Ignition Timing"],
		'units': [" PSI", " g/s", "°", "°", " %", "°"]
	}
}

class RootWidget(BoxLayout):
	# This class holds the ScreenManager and the sidebar with buttons.
	
	screen_manager = ObjectProperty(None)	# reference to ScreenManager instance
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# set the initial data for the home screen
		self.ids.screen_manager_id.get_screen('home').set_sensor_data(
			SENSOR_CONFIGS['home']['names'],
			SENSOR_CONFIGS['home']['units']
		)
		
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
					active_screen.set_sensor_data(config['names'], config['units'])
				else:
					print(f"No sensor configuration found for screen: {screen_name}")
			else:
				print(f"Screen '{screen_name}' does not have a 'set_sensor_data' method.")

class MainApp(App):
	def build(self):
		return RootWidget()

if __name__ == '__main__':
	MainApp().run()
