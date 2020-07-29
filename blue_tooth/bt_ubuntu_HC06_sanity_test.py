import bluetooth, subprocess
target_name = "HC-06"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices: 
    print(bdaddr)
    print(bluetooth.lookup_name( bdaddr ))
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print("found target bluetooth device with address "+ target_address)
else:
    print("could not find target bluetooth device nearby")



# Now, connect in the same way as always with PyBlueZ
try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((target_address,1))
except bluetooth.btcommon.BluetoothError as err:
    # Error handler
    pass
VALID_COMMANDS={
"1" : "test motor 1",
"2" : "test motor 2",
"3" : "test motor 3",
"3" : "test motor 4",
"l" : "left turn",
"r" : "right turn",
"f" : "forward",
"b" : "reverse",
"s" : "stop"

}
cmd=0
while True:
	cmd=input("Enter the command  :  ");
	if cmd not in VALID_COMMANDS.keys():
		print("please use valid commands")
		print(VALID_COMMANDS)
	s.send(cmd)
	print("sent cmd  :"+cmd)

s.close()
