# obd2-dash
> Raspberry Pi 4 based Car Dashboard that displays OBD-II information on a convenient, modern-looking dashboard. Running on Ubuntu Server + LXDE desktop environment.

![alt text](https://github.com/jpsullivan234/obd2-dash/blob/main/src/utils/dashboard-preview.png "dashboard preview")

---

**Hardware:**
- Raspberry Pi 4
- Official 7" RPI Touch Screen
- OBD-II to USB adapter
    - ([This](https://www.amazon.com/bbfly-BF32301-OBD-II-Windows-Diagnostic-Scanner/dp/B01N22B3FQ) is the one I am using, but double-check that it works with your car!)

**Getting Started:**
1. SSH into your Raspberry Pi. NOTE: this program uses a GUI, so the pi must have some sort of desktop environment installed. I used LXDE.
2. Clone this repository using the Pi SSH terminal
4. Navigate to the project directory, create a new virtual environment, and activate it (paste and run the following code in the terminal):
   ```
   python -m venv venv
   ```
   ```
   source venv/bin/activate
   ```
5. Run this line in the terminal to install the required python libraries:
   ```
   pip install -r ~/obd2-dash/requirements.txt
   ```
6. Connect the pi to your car via the OBD-II adapter and run the following line in the terminal:
   ```
   python src/main.py
   ```
   You should see the GUI window pop up. The OBD-II's status will appear at the top of the screen.
   The dashboard will be populated with random values if the OBD-II adapter is not connected

---


*This is an ongoing project and is not perfect by any means! Feel free to play around and change stuff!!*
   
