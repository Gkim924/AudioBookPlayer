import RPi.GPIO as GPIO

# Pin assignments

readyLedPin = 12
playingLedPin = 7
playButtonPin = 16
rewindButtonPin = 11
fastForwardButtonPin = 15

playerState = 'Paused'

def playPause(buttonState):
    global playerState
    
    # Change LED Status
    if GPIO.input(readyLedPin) == GPIO.HIGH:
        GPIO.output(readyLedPin, GPIO.LOW)
        GPIO.output(playingLedPin, GPIO.HIGH)
    else:
        GPIO.output(readyLedPin, GPIO.HIGH)
        GPIO.output(playingLedPin, GPIO.LOW)

    # Update internal status
    if playerState == 'Paused':
        playerState = 'Playing'
    else:
        playerState = 'Paused'

    print('Playback:  ' + playerState)


def redLedTest(buttonState):
    if GPIO.input(playingLedPin) == GPIO.HIGH:
        GPIO.output(playingLedPin, GPIO.LOW)
    else:
        GPIO.output(playingLedPin, GPIO.HIGH)


def rewind(buttonState):
    print('Rewinding 30s...')

def fastForward(buttonState):
    print('Fast Forwarding 30s...')

# Configure GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(readyLedPin, GPIO.OUT)
GPIO.setup(playingLedPin, GPIO.OUT)

GPIO.setup(playButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rewindButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fastForwardButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(playButtonPin,GPIO.RISING, callback=playPause, bouncetime=200)
GPIO.add_event_detect(rewindButtonPin, GPIO.RISING, callback=rewind, bouncetime=200)
GPIO.add_event_detect(fastForwardButtonPin, GPIO.RISING, callback=fastForward, bouncetime=200)

print('Player Starting...')
print('Playback:  ' + playerState)
# Turn on LED to indicate ready status
GPIO.output(readyLedPin, GPIO.HIGH)


try:
    while True: 
        continue

except:
    print('\n')
    print('Exiting...')
    print('Cleaning up GPIO...')
    GPIO.cleanup()


    

    