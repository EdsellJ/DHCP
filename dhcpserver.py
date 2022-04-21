from socket import *
#from ipaddress import IPv4Address
import datetime

serverPort = 18000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

#creating a client class to hold information about clients
class Record:
    def __init__(self, clientMac):
        self.clientMac = clientMac
        #a timesteamp is added whenever a new mac is added to the records
        self.setTimestamp()
    clientIP = '0.0.0.0'
    acked = False

    def releaseIP(self):
        self.acked = False #reset Acked
        self.timestamp = datetime.datetime.now()
        print("\t - IP released")

    def renewIP(self):
        self.acked = True
        self.setTimestamp()
        print("\t - reset timestamp")
        print("\t - set acked to 'True'")

    
    def setTimestamp(self):
        self.timestamp = datetime.datetime.now() + datetime.timedelta(0,60)

    def displayClientDetails(self):
        print("\n_______________")
        print("Client Details:")
        print("_______________")
        print("MAC:\t\t", self.clientMac)
        print("IP:\t\t", self.clientIP)
        print("Timestamp:\t", self.timestamp)
        print("acked:\t\t", self.acked)
        print("_______________")
        print("")

addresses = [['192.168.45.1', False],['192.168.45.2', False],['192.168.45.3', False],['192.168.45.4', False],
            ['192.168.45.5', False], ['192.168.45.6', False],['192.168.45.7', False], ['192.168.45.8', False],
            ['192.168.45.9', False], ['192.168.45.10', False], ['192.168.45.11', False], ['192.168.45.12', False],
            ['192.168.45.13', False], ['192.168.45.14', False]]


#searches for an available ip address
def findIP():
    for i in range(len(addresses)):
        if addresses[i][1] == False:
            addresses[i][1] = True
            return addresses[i][0]
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
        
        #find if the MAC is in the records and record its index int the list
        listIndex = searchRecord(recordList, lambda x: x.clientMac == message[1])

        #Switch to handle different message types
        match int(messageType):

            #3. DISCOVER case
            case 0:
                print("received DISCOVER")

                
                            
                #a. if MAC has an IP assigned 
                if listIndex != -1:
                    print("\t - MAC already in record")

                    #display info
                    recordList[listIndex].displayClientDetails()

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
                        recordList[listIndex].setTimestamp()
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
                        recordList[listIndex].clientIP = availIP #add ip to record
                        print("\t - adding MAC, IP, and timestamp to the record")

                        #display info
                        recordList[listIndex].displayClientDetails()
                        #send offer
                        print("sending OFFER")
                        returnMessage = '0' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                        serverSocket.sendto(returnMessage.encode(), clientAddress)

                    #e. if there are no available IP's
                    else:
                        print("\t - all ip's are assigned")
                        #if there are any expired timestamps
                        if listIndex != -1:
                            print("\t - found an expired timestamp")
                            print("\t - replacing old record with updated mac and timestamp")
                            print("setting acked to 'False'")
                            recordList[listIndex].setTimestamp()
                            recordList[listIndex].clientMac = message[1]
                            recordList[listIndex].acked = False
                            #send offer
                            print("sending OFFER")
                            returnMessage = '0' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                            serverSocket.sendto(returnMessage.encode(), clientAddress)
                        
                        #f. if all IP's are within the timestamp
                        else:
                            #send decline message
                            returnMessage = '2' + ','
                            serverSocket.sendto(returnMessage.encode(), clientAddress)


                        


            #REQUEST case
            case 1:
                print("received REQUEST")
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

                        #display info
                        recordList[listIndex].displayClientDetails()

                    #send the decline messages 
                    else:
                        returnMessage = '2' + ','
                        serverSocket.sendto(returnMessage.encode(), clientAddress)
                        
                else:
                    returnMessage = '2' + ','
                    serverSocket.sendto(returnMessage.encode(), clientAddress)
            
            #RELEASE case
            case 2:
                print("recieved RELEASE")
                if listIndex != -1: #if the Mac is found in the vector
                    #release IP
                    recordList[listIndex].releaseIP()

                    #display info
                    recordList[listIndex].displayClientDetails()
                    

            #RENEW case
            case 3:
                print("recieved RENEW")
                if listIndex != -1: #if the Mac is found in the vector
                    #renew IP
                    recordList[listIndex].renewIP()

                    #display info
                    recordList[listIndex].displayClientDetails()

                    #send Acknowledge messagse
                    print("sending ACKNOWLEDGE")
                    returnMessage = '1' + ',' + recordList[listIndex].clientMac + ',' + recordList[listIndex].clientIP + ',' + str(recordList[listIndex].timestamp)
                    serverSocket.sendto(returnMessage.encode(), clientAddress)
            
            #LIST case
            case 4:
                print("recieved LIST")
                print(" - sending record data")

                #create message
                returnMessage = ""
                for i in range(len(recordList)):
                    returnMessage = returnMessage + recordList[i].clientMac + ',' + recordList[i].clientIP + ',' + str(recordList[i].timestamp) + ',' + str(recordList[i].acked) + ','

                #send message
                serverSocket.sendto(returnMessage.encode(), clientAddress)

            case _:
                print("message not recognized")
                continue
       
if __name__ == "__main__":
    main()