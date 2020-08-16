# ego1_repo_root
ego one bot related content

Current status: In summary when you run the flask application, it starts a web server(__init__.py) and the launches a page (templates/controller.html) has a live video stream from raspberry pi cam and few buttons to control the bot's movement
to view page : ip_address:8080/ego_ctrl/controller

1.arduino_programs : talks to the motor driver (PWM etc)
a. manual_loop_test_with_bluetooth.ino
  Serial3 is connected to HC06 bluetooth module
  CommandHandler library from github is used to handle commands to the bluetooth module
    "turn","stop","forward","reverse","reverse turn" i.e it has , run forward or turn while in forward motion, run reverse or run while in reverse motion, depending on what you     feed into left and right pwm it turns accordingly.
    A higher level (python) program is supposed to take care of the command conversions.
    
  copy_of_sriram_libs/arduino_connections.h has the pin defines
  copy_of_sriram_libs/motor_control.c has the motor control functions that drive to the pwm pins
  The folder is named copy as these are in libraries folder of arduino download and i created a softlink to them
  
2. Website and Python bluetooth connection and command reception
web/flask-project/flaskr
  ../useful_commands_lan has the command to invoke flask application ( export flask, flask run etc)
  __init__.py is the main flask file ( this was created following flask tutorial) to create the webserver
    custom code is : from flaskr.bluetooth_connector_hc06 import BluetoothConnectorHC06  : this scans and connects to HC06 bluetooth module
    custom code is : from flaskr.bot_controller import BotController : which has an FSM to control the movement of the BOT
  botController.py
    implements an FSM which starts with a "STOP" state, from where it moves to various states "FORWARD", "REVERSE", "TURN_LEFT", "TURN_RIGHT"
    usage:
    bot=BotController()
    bot.on_cmd_reception("move_forward") // moves through FSM and sets the required commadn in bot.cmd_to_send) ( read below bluetooth module for full usage)
  Bluetooth_keyboard_ctrl_test.py
    usage:
    bt_conn=BluetoothConnectorHC06()
    bt_socket=None
    if(bt_conn.scan_for_devices()==1):
	    bt_socket=bt_conn.connect_bluetooth()
    else:
	    print("bluetooth connection failed")
	  exit()
 for the weblink and webpage
    ego_ctrl.py
      routes /controller page
    base.html      ( base templates for all pages : from tutorial)  
    templates/auth ( from tutorial)
    templates/blog ( from tutorial)
    templates/ego_ctrl/controller.html
        has the buttons and serves socketio links and commands
   summary: from webpage js sends "forward" call
    @socketio.on('forward') 
    def on_forward():
	    print("socket rcvd : forward")
	    bot.on_cmd_reception("move_forward")
	    bt_socket.send(bot.cmd_to_send)
      
      
3.For embedding video in the web page , 
to generate video three ways were tried
  1. run "ego1_repo_root/ego0_backup/ego/scripts/rasp_cam : shows the video output of camera in a link that is output when you run the script
  2. web/flask-project/flaskr/camera.py, camera_pi.py, base_camera.py to use picamera python library to embed a stream 
     usage: refer to __init_py commented out section CAMERA
     @app.route('/video_feed')
     def video_feed():
     """Video streaming route. Put this in the src attribute of an img tag."""
     return Response(gen(Camera()),
  3. web/live_stream/rasp_stream.sh : streams output to port 5000
  credit : https://github.com/jacksonliam/mjpg-streamer
    #!/bin/bash
    cd /home/pi/bot_tmp/mjpg-streamer/mjpg-streamer-experimental
    ./mjpg_streamer -o "output_http.so -w ./www -p 5000" -i "input_raspicam.so -rot 180 "

To embed the video stream:
   usage : web/flask-project/flaskr/templates/controller.html
   <img  src="http://127.0.0.1:5000?action=stream" title="Title of image" alt="alt text here"/>
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
***************************************************************************************************************
FILE CONTENT
***************************************************************************************************************
ego1_repo_root/

     /arduino_programs:
		/copy_of_sriram_libs
			/arduino_definitions.h
			/motor_control.c
		/manual_loop_test_with_bluetooth
		/simple_motor_test_with_bluetooth
		/simple_motor_test_with_serial
     /bluetooth:
		/bluetooth_connector.py
		/bt_keyboard_ctrl_test.py
		/bt_ubuntu_HC06_sanity_test
		/read_keybaord.py
		/raspberry_cmd_line_bt_enable.txt
		
    /ego0_backup
	      /ego
		/demorad
			/Python
			/board_connect_sanity.py
			/demorad_linux  #files copied from demorad pendrive out of the box
		/demorad_linux	
		/scripts
			/callMPU.py
			/dhcpcd.conf
			/gps.py
			/manual_gui.py
			/manual_guiv2.py
			/mpu.py
			/pyserialcmd.txt
			/rajib.py
			/rajib_orig.py
			/rasp_cam.py    #mjpg streamer based video stream to a web port
			
     dependencies : dependencies for python etc
     README.md 

    /web

    /flask-project # files in flask application:
    	/flaskr
		/auth.py ( from tutorial : for log in authentication)
    		/blog.py ( from tutorial : to create blogs)
    		/db.py   ( from tutorial : sql database  )
		/bluetooth_connector_hc06.py
		/bot_controller.py
    		/camera, camera_Pi, base_camera : trials to make use of picamera python module to get streaming from raspberry pi cam
    		/test_bt.py : to just test the usage of bot_controller and bluetooth connector without bringing up any webserver
		/templates
			/auth
			/blog
			/ego_ctrl
				controller.html
			base.html
		/static
			style.css
	/useful_cmd_in_lan : commands to launch flask project
	/useful_cmd_port_forwarded : if you want to do port forwarding to access the flask url from outside lan use this
	
    /live_stream
        rasp_stream.sh: to launch mjpg streamer : credit : https://github.com/jacksonliam/mjpg-streamer
    /port_forwarding_commands.txt : to forward urls to outside lan
