import ipaddress
from socket import *
import re, uuid
import datetime

serverName = '192.168.1.69'
serverPort = 18000
clientMac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
clientSocket = socket(AF_INET, SOCK_DGRAM)




def main():
    #Send a DISCOVER Message
    print("Sending LIST")
    messageType = '4'
    message = messageType + ',' 
    clientSocket.sendto(message.encode(),(serverName, serverPort))

    #wait for return message and parse
    returnMessage, serverAddress = clientSocket.recvfrom(2048)
    returnMessage = returnMessage.decode().split(",")

    #Print client Information
    for i in range(int((len(returnMessage) - 1)/4)):
        print("\n_______________")
        print("Client", i+1, ": ")
        print("_______________")
        print("MAC:\t\t", returnMessage[(i*4)]) #1, 5 , ...
        print("IP:\t\t", returnMessage[(i*4) + 1]) #2, 6 , ...
        print("Timestamp:\t", returnMessage[(i*4) + 2]) #3, 7 , ...
        print("acked:\t\t", returnMessage[(i*4) + 3]) #4, 8 , ...
        print("_______________")
        print("")


if __name__ == "__main__":
    main()