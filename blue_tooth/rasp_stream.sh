#!/bin/bash
cd /home/pi/bot_tmp/mjpg-streamer/mjpg-streamer-experimental
./mjpg_streamer -o "output_http.so -w ./www -p 5000" -i "input_raspicam.so -rot 180 "
