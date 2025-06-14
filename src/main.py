from kivy.app import App
from kivy.app import Builder
from kivy.uix.boxlayout import BoxLayout
from gui.screens.dashboard import DashboardScreen

class MainLayout(BoxLayout):
	pass

class ObdDashboardApp(App):
	def build(self):
		Builder.load_file("src/gui/kv/main.kv")
		return MainLayout()

if __name__ == "__main__":
	ObdDashboardApp.run()
