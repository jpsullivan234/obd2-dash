import obd

# create connection
connection = obd.OBD('/dev/ttyUSB0')

# select a command
cmd = obd.commands.RPM

# send the command
response = connection.query(cmd)

print(f"RPM: {response.value}")
