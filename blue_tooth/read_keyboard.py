from pynput.keyboard import Key, Listener

def on_press(key):
	try:	
		if key== key.up:
			print("up")
		elif key==key.down:
			print("down")
		elif key==key.space:
			print("stop")
		elif key==key.left:
			print("left")
		elif key==key.right:
			print("right")
				
	except AttributeError:
		print("attribute error")
		if key.char=='f':
			print("forward")
		elif key.char=='r':
			print("reverse")

def on_release(key):
	#print('{0} release'.format(key))
	if key == Key.esc:
        # Stop listener
        	return False

# Collect events until released
with Listener(on_press=on_press,on_release=on_release) as listener:
	listener.join()
