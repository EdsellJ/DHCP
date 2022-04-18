from socket import *
from ipaddress import IPv4Address

serverPort = 18000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

adresses = [('192.168.45.1', False), ('192.168.45.2', False),('192.168.45.3', False),('192.168.45.4', False),
            ('192.168.45.5', False), ('192.168.45.6', False),('192.168.45.7', False), ('192.168.45.8', False),
            ('192.168.45.9', False), ('192.168.45.10', False), ('192.168.45.11', False), ('192.168.45.12', False),
            ('192.168.45.13', False), ('192.168.45.14', False)]
#creating a client class to hold information about clients
class Record:
    def __init__(self, clientMac):
        self.clientMac = clientMac
    clientIP = '0.0.0.0'
    #timestamp
    acked = False


    
def main():
    print ('The server is ready to receive')
    #create an empty list to hold Records objects
    records = []

    while 1:
        """
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        """
        message, clientAddress = serverSocket.recvfrom(2048) #receive message
        message = message.decode().split(",") #decode and split message
        messageType = message[0] #find the type of message being sent

        match int(messageType):
            #DISCOVER
            case 0:
                if len(records) == 0:
                    records.append(Record(message[1]))
                elif 
            case _:
                print("message not recognized")
                continue
        """
        if messageType ==  "DISCOVER":
            #if there are no records yet add one
            if len(records) == 0:
                records.append(Record(message[1]))
        """
        print(records[0].clientMac)
if __name__ == "__main__":
    main()