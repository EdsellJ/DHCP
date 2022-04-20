from socket import *
#from ipaddress import IPv4Address
import datetime

serverPort = 18000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

addresses = [['192.168.45.1', False],['192.168.45.2', False],['192.168.45.3', False],['192.168.45.4', False],
            ['192.168.45.5', False], ['192.168.45.6', False],['192.168.45.7', False], ['192.168.45.8', False],
            ['192.168.45.9', False], ['192.168.45.10', False], ['192.168.45.11', False], ['192.168.45.12', False],
            ['192.168.45.13', False], ['192.168.45.14', False]]

#creating a client class to hold information about clients
class Record:
    def __init__(self, clientMac):
        self.clientMac = clientMac
        #a timesteamp is added whenever a new mac is added to the records
        self.timestamp = datetime.datetime.now() + datetime.timedelta(0,60)
    clientIP = '0.0.0.0'
    acked = False

#searches for an available ip address
def findIP():
    for i in addresses:
        if addresses[0][1] == False:
            addresses[0][1] = True
            return addresses[0][0]
    return 'NONE'

#meathod to search the record list and return the index of a Record object
def searchRecord(list, filter):
    index = -1
    for x in list:
        index += 1
        if filter(x):
            return index
    return -1
   
def main():
    print ('The server is ready to receive')
    #create an empty list to hold Records objects
    recordList = []

    while 1:
        message, clientAddress = serverSocket.recvfrom(2048) #receive message
        message = message.decode().split(",") #decode and split message
        messageType = message[0] #find the type of message being sent

        #Switch to handle different message types
        match int(messageType):
            #DISCOVER
            case 0:
                #if no recordList exist
                if len(recordList) == 0:
                    recordList.append(Record(message[1])) #add mac and timestamp to record
                    recordList[0].clientIP = findIP() #add ip to record
                    #tkif theIP == 'NONE':
                        #do something
                    returnMessage = '0' + ',' + recordList[0].clientMac + ',' + recordList[0].clientIP + ',' + str(recordList[0].timestamp)
                    serverSocket.sendto(returnMessage.encode(), clientAddress)
                #check if MAC has an IP assigned yet
                #elif 
            #REQUEST
            case 1:
                ############################################################
                #working here!!!!

                print("received REQUEST")
                #find MAC is in the records and check if the associated IP matches the REQUEST
                listIndex = searchRecord(recordList, lambda x: x.clientMac == message[1])
                if recordList[listIndex].clientIP == message[2]:
                    print("\t - IP's match")
                    if datetime.datetime.now() < recordList[listIndex].timestamp:
                        print("\t - within time limit")
                        #set acked to true
                        recordList[listIndex].acked = True
                        print("\t - set Acked to true")
                        #send Acknowledge messagse
                        returnMessage = '1' + ',' + recordList[0].clientMac + ',' + recordList[0].clientIP + ',' + str(recordList[0].timestamp)
                        serverSocket.sendto(returnMessage.encode(), clientAddress)
                    #send the decline messages 
                    else:
                        returnMessage = '2' + ','
                        serverSocket.sendto(returnMessage.encode(), clientAddress)
                        
                else:
                    returnMessage = '2' + ','
                    serverSocket.sendto(returnMessage.encode(), clientAddress)
                    
            case _:
                print("message not recognized")
                continue
       
if __name__ == "__main__":
    main()