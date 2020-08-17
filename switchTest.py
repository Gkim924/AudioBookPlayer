import RPi.GPIO as GPIO

ledPin = 12
buttonPin = 16
buttonState = True

def my_callback(channel):
    global buttonState
    print('Button Pressed... %s'%channel)
    buttonState = not buttonState
    if buttonState == False:
        GPIO.output(ledPin, GPIO.HIGH)
    else:
        GPIO.output(ledPin, GPIO.LOW)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=my_callback, bouncetime=200)
print('Player Starting...')

while True: 

    continue

    

    