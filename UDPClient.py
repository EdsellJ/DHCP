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
    print("Sending Discover Message")
    messageType = '0'
    message = messageType + ',' + clientMac
    clientSocket.sendto(message.encode(),(serverName, serverPort))

    while 1:
        #wait for return message and parse
        returnMessage, serverAddress = clientSocket.recvfrom(2048)
        returnMessage = returnMessage.decode().split(",")
        
        messageType = returnMessage[0]
        match int(messageType):
            #OFFER
            case 0:
                print("received OFFER")
                #check for matching MAC address
                if(returnMessage[1] == clientMac):
                    print("\t - MAC matches")
                    #check for timestamp
                    if(datetime.datetime.now() < datetime.datetime.strptime(returnMessage[3], '%Y-%m-%d %H:%M:%S.%f')):
                        print("\t - within time limit")
                        #send REQUEST message
                        print("sending REQUEST")
                        messageType = '1'
                        message = messageType + ',' + clientMac + ',' + returnMessage[2] + ',' + returnMessage[3]
                        clientSocket.sendto(message.encode(),serverAddress)
                    else:
                        print("Out of time: closing client")
                        clientSocket.close()
                else:
                    print("MAC does not match: closing client")
                    clientSocket.close()
            #ACKNOWLEGE case
            case 1:
                print("received ACKNOWLEDGE")
                #check for matching MAC address
                if(returnMessage[1] == clientMac):
                    print("\t - MAC matches")
                    print("IP: " + returnMessage[2] + " assigned to client")
                    ############################################
                    #client menu
                    # - Release
                    # - Renew
                    # - quit
                    while 1:
                        print("What would you like to do?\n")
                        print("(1): Release")
                        print("(2): Renew")
                        print("(q): quit")
                        userInput = input('Enter selection: ')
                        print(userInput)
                    
                        if userInput == '1':
                            messageType = '2'
                            message = messageType + ',' + clientMac + ',' + returnMessage[2] + ',' + returnMessage[3]
                            clientSocket.sendto(message.encode(),serverAddress)
                            print("IP released")

                        elif userInput == 2:
                            messageType = '3'
                            message = messageType + ',' + clientMac + ',' + returnMessage[2] + ',' + returnMessage[3]
                            clientSocket.sendto(message.encode(),serverAddress)
                            break

                        else:
                            print("Goodbye")
                            print("______________________")
                            clientSocket.close()
                            break
                        
                else:
                    print("MAC does not match")
                    clientSocket.close()

            #DECLINE
            case 2:
                print("Your Request has been declined")
                clientSocket.close()            
            case _:
                print("message not recognized")
                continue

    clientSocket.close()

if __name__ == "__main__":
    main()





