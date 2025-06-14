from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty

class MetricCard(BoxLayout):
	def __init__(self, metric_name, value='--', **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.padding = 10
		self.spacing = 5
		with self.canvas.before:
			Color(0.2, 0.2, 0.2, 1)
			self.rect = RoundedRectangle(radius=[20])
		self.bind(pos=self.update_rect, size=self.update_rect)

		self.label = Label(text=metric_name, font_size='16sp')
		self.value_label = Label(text=str(value), font_size='24sp', bold=True)
		self.add_widget(self.label)
		self.add_widget(self.value_label)

	def update_value(self, new_value):
		self.value_label.text = str(new_value)

	def update_rect(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size

class DashboardScreen(Screen):
	def on_enter(self):
		grid = self.ids.metrics_grid
		grid.clear_widgets()
		metric_names = ['RPM', 'Speed', 'Coolant Temp', 'Battery', 'Fuel', 'Throttle']
		for name in metric_names:
			grid.add_widget(MetricCard(metric_name=name))
