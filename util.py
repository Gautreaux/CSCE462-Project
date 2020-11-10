

# need to use a linux python build for uname to work?
import os

def isRaspi():
    l = str(os.uname())
    if("raspberrypi" in l):
        return True
    
    return not ("Microsoft" in l)