import RPi.GPIO as GPIO
import time
import thread
import websocket

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.OUT)

flashDuration = 10
active = False
lastMessage = 0

def on():
  global active
  GPIO.output(25, GPIO.HIGH)
  active = True
  print("Pin 25 HIGH")

def off():
  global active
  GPIO.output(25, GPIO.LOW)
  active = False
  print("Pin 25 LOW")

def on_message(ws, message):
  global lastMessage
  print("WS: Message Recieved")
  lastMessage = time.time()

def on_error(ws, err):
  print("Connection error") 
  print(err)

def on_close(ws):
  print("Connection closed")

def on_open(ws):
  print("Connected...")

def open_connection():
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("ws://exp.endoflow.com:3102/socket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
  ws.on_open = on_open
  ws.run_forever()

def run_loop():
  global lastMessage
  global active

  while 1:
    # If the last message was more than `flashDuration` seconds ago, turn off the light
    diff = time.time() - lastMessage
    print(active, lastMessage, diff)
    if active and diff > flashDuration:
      off()
    elif not active and diff < flashDuration:
      on()
    time.sleep(0.1)

if __name__ == "__main__":
  thread.start_new_thread(run_loop, ())
  open_connection()
