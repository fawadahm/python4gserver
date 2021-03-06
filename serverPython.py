import socket
import sys
import thread
from datetime import datetime


# Socket Program for Server


###################### FUNCTIONS ###############################

# Sender Handler Function
def senderHandler(senderFD):
    # This function will handle the app sending the data
    # It will store data sent by the app and relay it to the receiver
    # Stay in this loop and wait for data
    dataReceived = 0  # Specifies the amount of data we have collected

    global senderBuffer
    global endOfFile
    global fileSize
    global senderCounter
    global receiverCounter

    senderBuffer = ''
    global sendData
    # Stay in this loop forever and wait for data
    #print 'SenderHandler : Receiving Data'
    global timeLog

    startTime = datetime.utcnow()
    endTime = datetime.utcnow()

    while endOfFile is False:
        # store data in sender buffer
        tempBuffer = senderFD.recv(1024 * 1024)
        # Record the number of bytes we have received
        dataReceived = dataReceived + sys.getsizeof(tempBuffer)
        fileSize = dataReceived
        # Put the data in the sender buffer
        senderBuffer = tempBuffer + senderBuffer

        # If there is nothing in the buffer, then the transfer is complete
        if tempBuffer == '':
            # There was an on-going connection and now it has reached the end-of-file
            endOfFile = True
            endTime = datetime.utcnow() # note the end time

    receivingTime = endTime - startTime
    #receivingTime = datetime.timestamp
    print ('SenderHandler : Received = ' + str(dataReceived/(1000*1000.0)) + " MB and Time Interval = "
           +str(receivingTime) + " s")
    # print ('SenderHandler : Flow Completion Rate  = ' + str(dataReceived/(receivingTime*1000.0*10000)))

    # timeLog.write('SenderHandler : File Size = ' + str(dataReceived) + ' Time ' + str(receivingTime))
    timeLog.write('\nFile Size = ' + str(dataReceived/(1000*1000.0)) + ", " + ' Interval = ' + str(receivingTime) +
                  ', Start Time = ' + str(startTime) + ', End Time = ' + str(endTime) + '')




    # print ("SenderHandler : Sender Counter = " + str(senderCounter) + " Receiver Counter = " + str(receiverCounter))


    return


# Receiver Handler Function
def receiverHandler(receiverFD):
    # This function will handle the app receiving the data
    global sendData
    global fileSize
    global senderConnected
    global receiverCounter
    # print 'Receiver Handler with ' + str(receiverFD) + str(sendData)

    done = False

    global senderBuffer
    global endOfFile
    global fileSize
    dataSent = 0
    sentData = 0

    print ('ReceiverHandler : Waiting')

    global timeLog
    # Stay in this loop until sender isn't connected
    while senderConnected is False:
        pass  # Waiting for sender


    # printOnce = True

    # while receiverCounter > senderCounter:
        # if (printOnce):
          #   print ("ReceiverHandler : Stuck here")
            # print ("ReciverHandler: Receiver Counter = " + str(receiverCounter) + " : Sender Counter = " + str(senderCounter))
           #  printOnce = False
        # pass
        # Stay in the loop until sender is connected and ready to go

    bufferSize = 1024 * 1024
    flag = 0

    print ('Sending bytes now')
    startTime = datetime.utcnow()

    bytesSent = 0

    while (endOfFile is not True) or (bytesSent < fileSize):
        #while (sys.getsizeof(senderBuffer)<1024*1024):
         #   pass
        receiverFD.sendall(senderBuffer)
        bytesSent = bytesSent + sys.getsizeof(senderBuffer)
        senderBuffer = ''
        print ("sent = " +str(bytesSent/(1000*1000.0)))
        #print ('Sending')



    #while ((sendBuffer = sendfile.read()) != ''):
     #   sendBuffer = sendfile.read()
      #  print ('File read')

    print ('Bytes sent ' + str(bytesSent))
    endTime = datetime.utcnow()
    # if the connection has already been established between sender & server
    # while onGoingConnection is True:
    #     # Stay in the loop until there is data to send
    #     while sentData < fileSize:
    #         sentData = sentData +sys.getsizeof(senderBuffer)
    #         try:
    #             receiverFD.sendall(senderBuffer)
    #         except:
    #             pass
    #             #print 'Exception here'
    #         senderBuffer = ''
    #     else:
    #         if endOfFile is True:
    #             # If all data has been sent, first make sure that the sender connection has been reset
    #             endTime = datetime.utcnow()
    #             break

    timeInterval = endTime - startTime
    print ('ReceiverHandler : Sender Sent = ' + str(sys.getsizeof(senderBuffer)/(1000*1000.0)) +
           " MB and Time Interval = " + str(timeInterval))
    # print ('ReceiverHandler : Sender : Time = ' + str(timeInterval))
    timeLog.write('\nSender : File Size = ' + str(sentData) + ' Time ' + str(timeInterval))
    timeLog.write('\nSender : Start Time = ' + str(startTime) + ' End Time = ' + str(endTime))


    # print ("ReceiverHandler : Receiver Counter = " + str(receiverCounter+1))
    receiverCounter += 1
    print ("ReceiverHandler: ReceiverCounter = " + str(receiverCounter) + ", SenderCounter = " + str(
        senderCounter))

    return


#################################################################



###################### DECLARATIONS ##########################


endOfFile = False
onGoingConnection = False

port = 1111  # This is the port we want to bind on
noOfConnectedDevices = 0  # number of devices connected to server
DEVICE_LIMIT = 2  # limit on the number of devices
senderBuffer = ''  # buffer for storing data from sender to receiver
sendData = False
endOfFile = False
fileSize = 0
timeLog = open('FieldTests.txt', 'a')
senderConnected = False
senderCounter = 0
receiverCounter = 0
############################################################







#################### MAIN CODE ########################

serverSocket = socket.socket()  # Create the server socket
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()  # We want to bind to the same host
serverSocket.bind((host, port))  # Connect socket to same host & port
serverSocket.listen(10)  # back log
print 'Main Program : Waiting for a connection'
# Time to listen for connections

#


timeLog.write('\nSession = ' + str(datetime.utcnow().strftime('%H_%M_%S_%f')))

counter = 0


while True:
    print '\n\nMain Program : Waiting for new connections due to loop'
    while noOfConnectedDevices < DEVICE_LIMIT:

        # print 'Iteration = ' + str(noOfConnectedDevices)
        # Accept incoming connections
        try:
            # print ('Main Program : Waiting for connections with counter = ' + str(counter))
            (conn, addr) = serverSocket.accept()  # Wait for a connection from the Android Phone
            # print 'Main Program : Accepted connection'  # Connection has been established
            ID = conn.recv(1)
            # print 'Main Program : ID = ' + ID

            if ID == "S":
                # print ('Main Program : Calling Sender Handler with counter = ' +str(counter))
                senderConnected = True
                # noOfConnectedDevices += 1
                # print 'Number of Connected Devices = ' + str(noOfConnectedDevices)
                #global onGoingConnection
                onGoingConnection = True
                thread.start_new_thread(senderHandler, (conn,))
                #senderCounter += 1
                conn = 0

            # elif ID == "Receiver":
            else:
                # print ('Main Program : Calling Receiver Handler with counter = ' +str(counter))
                thread.start_new_thread(receiverHandler, (conn,))
                noOfConnectedDevices += 1
                conn = 0
                # print 'Number of Connected Devices = ' + str(noOfConnectedDevices)

            # else:
                #   conn.close()
                # print 'Closed connection because it had ID = ' + ID + " = " + str (ID)

        except socket.error, msg:
            print 'Failed: Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        # serverSocket.close()

        # print 'Main Program : In end of try with connections = ' + str(noOfConnectedDevices) + ' and device limit = ' + str(DEVICE_LIMIT)

    noOfConnectedDevices = 0
    counter += 1
while 1:
    pass
serverSocket.close()
