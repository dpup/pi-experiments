import time
import RPi.GPIO as GPIO

TRIG = 25
ECHO = 17

def log(msg):
  print msg

def micro_to_secs(us):
  return us / 1E6

def secs_to_micro(s):
  return s * 1E6

def micro_sleep(us):
  time.sleep(micro_to_secs(us))

def reading():
  # Activate the trigger pin for 10 microseconds.
  GPIO.output(TRIG, True)
  micro_sleep(10)
  GPIO.output(TRIG, False)

  # Wait for the echo pin to activate.
  while GPIO.input(ECHO) == 0:
    echoStart = time.time()

  # Wait until the echo pin deactivates.
  while GPIO.input(ECHO) == 1:
    echoEnd = time.time()
  
  return secs_to_micro(echoEnd - echoStart) / 58

def main():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(ECHO, GPIO.IN)
  GPIO.setup(TRIG, GPIO.OUT)
  GPIO.output(TRIG, False)

  time.sleep(1)

  for i in range(0, 100):
    log("Test " + `i` + " " + `reading()`)
    time.sleep(1.5)

  GPIO.cleanup()

if __name__ == "__main__":
  main()

