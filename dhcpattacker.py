import ipaddress
from socket import *
import re, uuid
import datetime

serverName = '192.168.1.69'
serverPort = 18000
clientMac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
clientSocket = socket(AF_INET, SOCK_DGRAM)

def main():
    for i in range(14):
        #Send a DISCOVER Message
        print("Sending DISCOVER")
        messageType = '0'
        clientMac = "DoS" + str(i)
        message = messageType + ',' + clientMac
        clientSocket.sendto(message.encode(),(serverName, serverPort))

if __name__ == "__main__":
    main()