import obd

# create connection
connection = obd.OBD('/dev/ttyUSB0')

if connection.is_connected():  # Ensure a connection is established.
    supported_cmds = connection.supported_commands
    for command in supported_cmds:
        print(command.name)  # Print the name of each supported command
else:
    print("OBD-II adapter not connected or car ignition is off.")