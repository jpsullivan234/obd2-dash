from kivy.app import App
from kivy.lang import Builder
from gui.screens.dashboard import DashboardScreen
from gui.screens.sidebar import Sidebar
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(Screen):
	pass

class ObdDashboardApp(App):
	def build(self):
		Builder.load_file("gui/kv/main.kv")
		return MainScreen()

if __name__ == '__main__':
	ObdDashboardApp().run()
