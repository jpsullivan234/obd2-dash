from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import os

Builder.load_file("src/gui/kv/main.kv")

class DashboardScreen(BoxLayout):
	current_catagory = "engine"

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.update_metrics("engine")

	def update_metrics(self, category):
		dummy_data = {
        		"engine": ["RPM", "Coolant Temp", "Oil Temp", "Load", "Timing", "MAF"],
			"fuel": ["Fuel Level", "Fuel Trim", "Range", "Consumption", "Injector Time", "Lambda"],
			"speed": ["Speed", "Accel", "GPS Speed", "Avg Speed", "Drive Time", "Idle Time"]
			}
		metrics = dummy_data.get(category, ["---"] * 6)
		for i in range(6):
			self.ids[f"metric_{i+1}"].text = metrics[i]

