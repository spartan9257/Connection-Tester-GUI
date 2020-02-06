import os

#Return true if ping was successful
def checkPing(host):
    count = 0
    while(count <= 2):
        response = os.system("ping -n 1 " + host)
        # and then check the response...
        if response == 0:
            pingStatus = True
            break
        else:
            print("Reattempting the connection...")
            pingStatus = False
            count = count + 1
    if pingStatus == False:
        print("Unable to connect to host after 3 attempts")
    return pingStatus