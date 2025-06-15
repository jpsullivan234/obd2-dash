from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
import random

class HomeScreen(Screen):
	"""
	Kivy Screen class which displays real-time OBD-II data in a grid layout.
	This screen updates automatically every second.
	"""
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		# Main layout for sensor data grid
		self.grid = GridLayout(
			cols=3,
			rows=2,
			padding=dp(20),
			spacing=dp(10),
			size_hint=(1, 1)
		)
		self.add_widget(self.grid)
		
		# Labels to display actual sensor data
		self.sensor_value_labels = []
		self.sensor_name_labels = []
		
		# these store currently active sensor names
		self._current_sensor_names = []
		self._current_sensor_units = []
		
		# Initialize 6 empty display boxes
		for _ in range(6):
			
			# Create a vertical box layout for each sensor's display
			sensor_display_box = BoxLayout(
				orientation='vertical',
				padding=dp(10)
			)
			
			# Add rounded rectangle background
			with sensor_display_box.canvas.before: # type: ignore
					Color(0.2, 0.2, 0.2, 1)
					rect_instruction = RoundedRectangle(
						pos=sensor_display_box.pos,
						size=sensor_display_box.size,
						radius=[dp(15)]
					)
			# Bind the pos & size of the rect to the BoxLayout's pos & size
			sensor_display_box.bind( # type: ignore
				pos=lambda instance, value, r=rect_instruction: setattr(r, 'pos', value),
				size = lambda instance, value, r=rect_instruction: setattr(r, 'size', value)
			)
			
			# Label for sensor name (shown at the top of the box)
			name_label = Label(
				text="Name", # placeholder txt
				font_size=dp(16),
				color=(0.7, 0.7, 0.7, 1),
				halign='center',
				valign='top',
				size_hint_y=0.3
			)
			self.sensor_name_labels.append(name_label)
			sensor_display_box.add_widget(name_label)
			
			# Label for actual sensor value
			value_label = Label(
				text='N/A',
				font_size=dp(28),
				color=(1, 1, 1, 1),
				halign='center',
				valign='middle',
				size_hint_y=0.7
			)
			self.sensor_value_labels.append(value_label)
			sensor_display_box.add_widget(value_label)
			
			# add completed box to grid
			self.grid.add_widget(sensor_display_box)
			
		# Schedule the update function to run every second
		Clock.schedule_interval(self.update_sensor_data, 1)
	
	def on_enter(self, *args):
		print(f"{self.name} entered.")
		Clock.schedule_interval(self.update_sensor_data, 1)
		
	def on_leave(self, *args):
		print(f"{self.name} left.")
		Clock.unschedule(self.update_sensor_data)
	
	def update_sensor_data(self, dt):
		
		mock_data_values = []
		for i, name in enumerate(self._current_sensor_names):
			unit = self._current_sensor_units[i] if i < len(self._current_sensor_units) else ""
			# Generate mock data based on sensor name to make it somewhat realistic
			if "RPM" in name:
				mock_data_values.append(f"{random.randint(700, 3000)}{unit}")
			elif "Speed" in name:
				mock_data_values.append(f"{random.randint(0, 120)}{unit}")
			elif "Fuel Level" in name or "Fuel Flow" in name or "Fuel Consumed" in name:
				mock_data_values.append(f"{random.randint(10, 90)}{unit}")
			elif "Temp" in name or "Temperature" in name:
				mock_data_values.append(f"{random.randint(80, 100)}{unit}")
			elif "Volts" in name or "Voltage" in name:
				mock_data_values.append(f"{random.uniform(12.0, 14.5):.1f}{unit}")
			elif "Pressure" in name or "PSI" in name:
				mock_data_values.append(f"{random.randint(30, 60)}{unit}")
			elif "Trim" in name:
				mock_data_values.append(f"{random.uniform(-5.0, 5.0):.1f}{unit}")
			elif "Lambda" in name:
				mock_data_values.append(f"{random.uniform(0.9, 1.1):.2f}{unit}")
			elif "Throttle Pos" in name:
				mock_data_values.append(f"{random.randint(0, 100)}{unit}")
			elif "Mass Air Flow" in name:
				mock_data_values.append(f"{random.uniform(0.5, 5.0):.2f}{unit}")
			elif "Timing Advance" in name:
				mock_data_values.append(f"{random.uniform(-10.0, 30.0):.1f}{unit}")
			else:
				mock_data_values.append("N/A")
		
		# Update each value label with new data
		for i, data_value in enumerate(mock_data_values):
			if i < len(self.sensor_value_labels):
				self.sensor_value_labels[i].text = data_value
			
	def set_sensor_data(self, names_list, units_list):
		"""
		Method to dynamically set the sensor names and units for the labels.
		This would be called by your main application logic based on the
		selected sidebar button.

		Args:
			names_list (list): A list of 6 strings representing the sensor names.
			units_list (list): A list of 6 strings representing the units for each sensor.
		"""
		if len(names_list) != 6 or len(units_list) != 6:
			print(f"Warning: set_sensor_data expects 6 names and 6 units, but received {len(names_list)} names and {len(units_list)} units.")
			# Adjust lists to match the number of display boxes (6) if they don't
			names_list = (names_list + ["N/A"] * 6)[:6]
			units_list = (units_list + [""] * 6)[:6]
		
		# Update the internal lists that update_sensor_data uses
		self._current_sensor_names = names_list
		self._current_sensor_units = units_list
		
		# Update teh test of the name labels
		for i in range(6):
			self.sensor_name_labels[i].text = f"{names_list[i]}:"
			# Reset value labels to N/A initially
			self.sensor_value_labels[i].text = "N/A"
		
		# Trigger an immediate update to populate with new mock data
		self.update_sensor_data(0)  #dt=0 means immediate