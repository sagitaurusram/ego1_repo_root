import bluetooth, subprocess


class BluetoothConnectorHC06:
    target_name = "HC-06"
    target_address = None
    s = None

    def scan_for_devices(self):
        nearby_devices = bluetooth.discover_devices()
        for address in nearby_devices:
            print(address)
            print(bluetooth.lookup_name(address))
            if self.target_name == bluetooth.lookup_name(address):
                self.target_address = address
                break
        if self.target_address is not None:
            print("found target bluetooth device with address " + self.target_address)
            return 1
        else:
            print("could not find target bluetooth device nearby")
            return 0

    '''
    if (target_address == None):
        target_address = "98:D3:91:FD:53:B3"
    '''

    # Now, connect in the same way as always with PyBlueZ
    def connect_bluetooth(self):
        try:
            self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.s.connect((self.target_address, 1))
        except bluetooth.btcommon.BluetoothError:
            # Error handler
            print("bluetooth socket not connected")
            return None
        return self.s
