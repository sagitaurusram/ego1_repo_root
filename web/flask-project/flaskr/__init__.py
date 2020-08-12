from importlib import import_module
import os
from flask import Flask, Response
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room,rooms,disconnect
from flaskr.bluetooth_connector_hc06 import BluetoothConnectorHC06
from flaskr.bot_controller import BotController
#from flaskr.camera_pi import Camera

#def create_app(test_config=None):
# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
SECRET_KEY='dev',
DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

#if test_config is None:
# load the instance config, if it exists, when not testing
#	app.config.from_pyfile('config.py', silent=True)
#else:
# load the test config if passed in
#	app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
	os.makedirs(app.instance_path)
except OSError:
	pass

# a simple page that says hello
@app.route('/hello')
def hello():
	return 'Hello, World!'

from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import blog
app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')

from . import ego_ctrl
app.register_blueprint(ego_ctrl.bp)
######################################################################SOCKET IO and BOT
bt_conn=BluetoothConnectorHC06()
bt_socket=None
if(bt_conn.scan_for_devices()==1):
	bt_socket=bt_conn.connect_bluetooth()
else:
	print("bluetooth connection failed")
	exit()

bot=BotController()

socketio=SocketIO(app)

@socketio.on('connect')
def test_connect():
	print("i am connected")


@socketio.on('message')
def on_message(data):
	print('I received a message')

@socketio.on('forward')
def on_forward():
	print("socket rcvd : forward")
	bot.on_cmd_reception("move_forward")
	bt_socket.send(bot.cmd_to_send)

@socketio.on('reverse')
def on_reverse():
	print("socket rcvd : reverse")
	bot.on_cmd_reception("move_reverse")
	bt_socket.send(bot.cmd_to_send)

@socketio.on('left')
def on_left():
	print("socket rcvd : left")
	bot.on_cmd_reception("turn_left")
	bt_socket.send(bot.cmd_to_send)

@socketio.on('right')
def on_right():
	print("socket rcvd : right")
	bot.on_cmd_reception("turn_right")
	bt_socket.send(bot.cmd_to_send)

@socketio.on('stop')
def on_stop():
	print("socket rcvd : stop")
	bot.on_cmd_reception("stop")
	bt_socket.send(bot.cmd_to_send)

@socketio.on('accelerate')
def on_accelerate():
	print("socket rcvd : accelerate")
	bot.on_cmd_reception("accelerate")
	bt_socket.send(bot.cmd_to_send)

@socketio.on('decelerate')
def on_decelerate():
	print("socket rcvd : decelerate")
	bot.on_cmd_reception("decelerate")
	bt_socket.send(bot.cmd_to_send)

###################################################################CAMERA
'''
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
'''
####################################################################################CAMERA END
#return app
if __name__=='__main__':
	socketio.run(app)