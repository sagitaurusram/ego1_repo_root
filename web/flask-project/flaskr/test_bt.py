from bluetooth_connector_hc06 import BluetoothConnectorHC06
from bot_controller import BotController

bt_conn=BluetoothConnectorHC06()
bt_socket=None
if(bt_conn.scan_for_devices()==1):
	bt_socket=bt_conn.connect_bluetooth()
else:
	print("bluetooth connection failed")
	exit()
bot=BotController()

try:
	while True:
		x=bot.wait_for_cmd()
		bot.on_cmd_reception(x)
		print("sending bluetooth command :",bot.cmd_to_send)
		bt_socket.send(bot.cmd_to_send)
except KeyboardInterrupt:
		bt_socket.send("stop;")
		bt_socket.close()