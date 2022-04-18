from socket import *
import re, uuid

serverName = 'localhost'
serverPort = 18000
clientMac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
clientSocket = socket(AF_INET, SOCK_DGRAM)

def main():
    #message = input('Input lowercase sentence:')
    print(clientMac)
    messageType = '0'
    message = messageType + ',' + clientMac
    print(message)
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    """
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print (modifiedMessage.decode())
    """
    clientSocket.close()

if __name__ == "__main__":
    main()





