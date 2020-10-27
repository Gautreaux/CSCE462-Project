#system library functions

import os

#get and return a list of all interface ips
def getAllInterfaceIPs() -> [str]:
    pipe = os.popen('hostname -I')
    r = pipe.read().strip().split(' ')
    return list(map(lambda x: x.strip(), r))

    