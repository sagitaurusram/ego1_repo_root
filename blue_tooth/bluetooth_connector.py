import bluetooth, subprocess

class HC06_BluetoothConnector():
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

        if(target_address==None):
            target_address="98:D3:91:FD:53:B3"

# Now, connect in the same way as always with PyBlueZ
        try:
            s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect((target_address,1))
        except bluetooth.btcommon.BluetoothError as err:
                # Error handler
                
            pass
