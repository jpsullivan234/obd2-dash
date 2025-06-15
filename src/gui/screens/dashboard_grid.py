from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

class Dashboard(Screen):
    """
    Kivy Screen class which displays real-time OBD-II data in a grid layout.
    This screen updates automatically every second.
    """
    
    def __init__(self, obd_manager_instance, **kwargs):
        super().__init__(**kwargs)
        self.obd_manager = obd_manager_instance
        
        # Main layout for sensor data grid
        self.grid = GridLayout(
            cols=3,
            rows=2,
            padding=dp(20),
            spacing=dp(10),
            size_hint=(1, 1)
        )
        self.add_widget(self.grid)
  
        # OBD Connection Status Label
        self.status_label = Label(
            text="OBD Status: Initializing...", # Initial text
            font_size=dp(12),
            color=(1, 1, 0, 1), # Yellow for connecting, green for connected, red for error
            size_hint_y=0.05, # Takes 10% of the screen height
            pos_hint={'top': 1}, # Position at the very top
            halign='center',
            valign='middle'
        )
        self.add_widget(self.status_label) # Add status label above the grid
        
        # Labels to display actual sensor data
        self.sensor_value_labels = []
        self.sensor_name_labels = []
        
        # these store currently active sensor names
        self._current_sensor_names = []
        self._current_sensor_units = []
        self._current_obd_commands = []
        
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
    
    def on_enter(self, *args):
        print(f"{self.name} entered.")
        Clock.schedule_interval(self.update_sensor_data, 1)
        
    def on_leave(self, *args):
        print(f"{self.name} left.")
        Clock.unschedule(self.update_sensor_data)
    
    def update_sensor_data(self, dt):
        
        # Update OBD status label
        self.status_label.text = self.obd_manager.get_status_text()
        self.status_label.coler = self.obd_manager.get_status_color()
  
        # Query data via obd manager
        data = self.obd_manager.query_data(
            self._current_obd_commands,
            self._current_sensor_units
        )
        
        # Update each value label with new data
        for i, data_value in enumerate(data):
            if i < len(self.sensor_value_labels):
                self.sensor_value_labels[i].text = data_value
            
    def set_sensor_data(self, names_list, units_list, obd_commands_list):
        """
        Method to dynamically set the sensor names and units for the labels.
        This would be called by your main application logic based on the
        selected sidebar button.

        Args:
            names_list (list): A list of 6 strings representing the sensor names.
            units_list (list): A list of 6 strings representing the units for each sensor.
        """
        if len(names_list) != 6 or len(units_list) != 6 or len(obd_commands_list) != 6:
            print(f"Warning: set_sensor_data expects 6 items for all lists. Adjusting.")
            # Adjust lists to match the number of display boxes (6) if they don't
            names_list = (names_list + ["N/A"] * 6)[:6]
            units_list = (units_list + [""] * 6)[:6]
            obd_commands_list = (obd_commands_list + [None] * 6)[:6]
        
        # Update the internal lists that update_sensor_data uses
        self._current_sensor_names = names_list
        self._current_sensor_units = units_list
        self._current_obd_commands = obd_commands_list
        
        # Update the text of the name labels
        for i in range(6):
            self.sensor_name_labels[i].text = f"{names_list[i]}:"
            # Reset value labels to N/A initially
            self.sensor_value_labels[i].text = "N/A"
        
        # Trigger an immediate update to populate with new mock data
        self.update_sensor_data(0)  #dt=0 means immediate