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
    j = -1
    for i in addresses:
        if addresses[j][1] != True:
            addresses[j][1] = True
            return addresses[j][0]
        else:
            print("increment IP list")
            j += 1
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

            #3. DISCOVER case
            case 0:
                print("received REQUEST")

                #find if the MAC is in the records and record its index int the list
                listIndex = searchRecord(recordList, lambda x: x.clientMac == message[1])
                            
                #a. if MAC has an IP assigned 
                if listIndex != -1:
                    print("\t - MAC already in record")

                    #b. if within time limit
                    if datetime.datetime.now() < recordList[listIndex].timestamp:
                        print("\t - within time limit") 
                        #set acked to true
                        recordList[listIndex].acked = True
                        print("\t - set Acked to true")
                        #send Acknowledge messagse
                        print("sending ACKNOWLEDGE")
                        returnMessage = '1' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                        serverSocket.sendto(returnMessage.encode(), clientAddress)

                    #c. if not within time limit
                    else:
                        print("\t - not within time limit")
                        #reset timestamp
                        print("\t - reset timestamp")
                        recordList[listIndex].timestamp = datetime.datetime.now() + datetime.timedelta(0,60)
                        #send offer
                        print("sending OFFER")
                        returnMessage = '0' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                        serverSocket.sendto(returnMessage.encode(), clientAddress)

                #d. if mac does not have an ip yet
                elif listIndex == -1:
                    print("\t - MAC is not in the record yet")
                    availIP = findIP()
                    if availIP != 'NONE':
                        recordList.append(Record(message[1])) #add mac and timestamp to record
                        recordList[listIndex].clientIP = findIP() #add ip to record
                        print("\t - adding MAC, IP, and timestamp to the record")
                        #send offer
                        print("sending OFFER")
                        returnMessage = '0' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                        serverSocket.sendto(returnMessage.encode(), clientAddress)

                    #e. if there are no available IP's
                    else:
                        print("\t - all ip's are assigned")
                        #if there are any expired timestamps
                        listIndex = searchRecord(recordList, lambda x: x.timestamp < datetime.datetime.now())
                        if listIndex != -1:
                            print("\t - found an expired timestamp")
                            print("\t - replacing old record with updated mac and timestamp")
                            print("setting acked to 'False'")
                            recordList[listIndex].timestamp = datetime.datetime.now() + datetime.timedelta(0,60)
                            recordList[listIndex].clientMac = message[1]
                            recordList[listIndex].acked = False
                            #send offer
                            print("sending OFFER")
                            returnMessage = '0' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                            serverSocket.sendto(returnMessage.encode(), clientAddress)
                        
                        #f. if all IP's are withing the timestamp
                        else:
                            #send decline message
                            returnMessage = '2' + ','
                            serverSocket.sendto(returnMessage.encode(), clientAddress)


                        


            #REQUEST case
            case 1:
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
                        print("sending ACKNOWLEDGE")
                        returnMessage = '1' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
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