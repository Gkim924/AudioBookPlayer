import RPi.GPIO as GPIO
import subprocess
import sys
from mpd import (MPDClient, CommandError)
from socket import error as SocketError

# Pin assignments
readyLedPin = 12
playingLedPin = 7
playButtonPin = 16
rewindButtonPin = 11
fastForwardButtonPin = 15
shutDownButtonPin = 31

playerState = 'Paused'

# Configure MPD connection settings
HOST = 'localhost'
PORT = '6600'
CON_ID = {'host':HOST, 'port':PORT}

# Play or Pause and update LED Status | Playing: Red , Paused/Waiting: Green
def playPause(buttonState, client):
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
        client.play()
    else:
        playerState = 'Paused'
        client.pause()

    print('Playback: ' + playerState)
  
######################################################
def redLedTest(buttonState):
    if GPIO.input(playingLedPin) == GPIO.HIGH:
        GPIO.output(playingLedPin, GPIO.LOW)
    else:
        GPIO.output(playingLedPin, GPIO.HIGH)
######################################################

# Rewind by 5 seconds
def rewind(buttonState, client):
    if playerState == 'Paused':
        return
    print('Rewinding 5s...')
    status = client.status()
    time = status["elapsed"]
    client.seekcur(float(time) - 5)

# Fast forward by 5 seconds
def fastForward(buttonState, client):
    if playerState == 'Paused':
        return
    print('Fast Forwarding 5s...')
    status = client.status()
    time = status["elapsed"]
    client.seekcur(float(time) + 5)

# Initialize GPIO. Pass in MPD client so that it can be routed to callbacks
def initGPIO(client):
    # Configure GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(readyLedPin, GPIO.OUT)
    GPIO.setup(playingLedPin, GPIO.OUT)

    GPIO.setup(playButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(rewindButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(fastForwardButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(shutDownButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(playButtonPin,GPIO.RISING, lambda playButtonPin, tmp_client=client:playPause(playButtonPin,tmp_client), bouncetime=200)
    GPIO.add_event_detect(rewindButtonPin,GPIO.RISING, lambda rewindButtonPin, tmp_client=client:rewind(rewindButtonPin,tmp_client), bouncetime=200)
    GPIO.add_event_detect(fastForwardButtonPin,GPIO.RISING, lambda fastForwardButtonPin, tmp_client=client:fastForward(fastForwardButtonPin,tmp_client), bouncetime=200)
    GPIO.add_event_detect(shutDownButtonPin,GPIO.RISING, lambda shutDownButtonPin, tmp_client=client:closePlayer(GPIO,tmp_client), bouncetime=200)

    print('GPIO Initialized...')

# Connect MPD client
def mpdConnect(client, con_id):
        """
        Simple wrapper to connect MPD.
        """
        try:
                client.connect(**con_id)
        except SocketError:
                return False
        return True

# Cleanup all connections and shut down player
def closePlayer(GPIO, client):
    print('\n')
    print('Cleaning up GPIO...')
    GPIO.cleanup()
    print('Cleaning up MPD...')
    status = client.status()
    if status["state"] == 'play':
        client.pause()
    client.close()                     # send the close command
    client.disconnect()                # disconnect from the server
    print('Exiting...')
    subprocess.call(['sudo','shutdown', '-h', 'now'], shell=False) # this shuts down. next line never executed
    sys.exit() # use this for debug

######################################################################################################

def main():

    ## MPD object instance
    client = MPDClient()
    mpdConnect(client, CON_ID)
    # Initialize GPIO
    initGPIO(client)

    print('MPD Connected...')
    book = client.currentsong()
    print('Playing: ', book['file'])

    print('Player Starting...')
    print('Playback: ' + playerState)
    # Turn on LED to indicate ready status
    GPIO.output(readyLedPin, GPIO.HIGH)
    GPIO.output(playingLedPin, GPIO.LOW)

    # Program loop
    try:
        while True: 
            continue

    except:
        closePlayer(GPIO, client)

# Script starts here
if __name__ == "__main__":
    main()
    

    