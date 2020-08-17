# IMPORTS
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
from time import sleep
from sys import exit

# Configure MPD connection settings
HOST = 'localhost'
PORT = '6600'
CON_ID = {'host':HOST, 'port':PORT}


## Some functions
def mpdConnect(client, con_id):
        """
        Simple wrapper to connect MPD.
        """
        try:
                client.connect(**con_id)
        except SocketError:
                return False
        return True

def main():
        ## MPD object instance
        client = MPDClient()
        mpdConnect(client, CON_ID)

        status = client.status()
        print status

        client.play()
        sleep(10)
        client.pause()
        
        client.close()                     # send the close command
        client.disconnect()                # disconnect from the server

        # while True:
        #         device = checkForUSBDevice("1GB") # 1GB is the name of my thumb drive
        #         if device != "":
        #                 # USB thumb drive has been inserted, new music will be copied
        #                 flashLED(0.1, 5)
        #                 client.disconnect()
        #                 loadMusic(client, CON_ID, device)
        #                 mpdConnect(client, CON_ID)
        #                 print client.status()
        #                 flashLED(0.1, 5)
        #                 # wait until thumb drive is umplugged again
        #                 while checkForUSBDevice("1GB") == device:
        #                         sleep(1.0)
        #                 flashLED(0.1, 5)
        #         if GPIO.input(BUTTON) == True:
        #                 if timebuttonisstillpressed == 0:
        #                         # button has been pressed, pause or unpause now
        #                         if client.status()["state"] == "stop":
        #                                 client.play()
        #                         else:
        #                                 client.pause()
        #                         updateLED(client)
        #                 elif timebuttonisstillpressed > 4:
        #                         # go back one track if button is pressed > 4 secs
        #                         client.previous()
        #                         flashLED(0.1, 5)
        #                         timebuttonisstillpressed = 0
        #                 timebuttonisstillpressed = timebuttonisstillpressed + 0.1
        #         else:
        #                 timebuttonisstillpressed = 0

        #         sleep(0.1)

# Script starts here
if __name__ == "__main__":
    main()