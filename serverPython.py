import socket
import sys
import thread

# Socket Program for Server


###################### FUNCTIONS ###############################

# Sender Handler Function
def senderHandler (senderFD):

	# This function will handle the app sending the data
	# It will store data sent by the app and relay it to the receiver
	# stay in this loop and wait for data
	print 'Sender Handler Thread with FD: ' + str (senderFD)

	global senderBuffer
	senderBuffer = ''
	global sendData
	while 1:
		# store data in sender buffer

		tempBuffer = senderFD.recv (1024)


		if (tempBuffer != ''):
			senderBuffer = tempBuffer + senderBuffer
			print 'Sender Handler : Received Data = ' + senderBuffer
			sendData = True
			print ('Send data = ' + str (sendData))







	return


# Receiver Handler Function
def receiverHandler (receiverFD):
	# This function will handle the app receiving the data
	global sendData
	print 'Receiver Handler with ' + str (receiverFD) + str (sendData)
	
	done = False

	global senderBuffer

	while (done == False):
		if (sendData == True):
			receiverFD.sendall (senderBuffer)
			done = True
			print 'Data sent'
		else:
			print 'Stuck here'


	return

#################################################################



###################### DECLARATIONS ##########################

port = 1111 # This is the port we want to bind on
noOfConnectedDevices = 0 # number of devices connected to server
DEVICE_LIMIT = 2 # limit on the number of devices
senderBuffer = '' # buffer for storing data from sender to receiver
sendData = False

############################################################







#################### MAIN CODE ########################

serverSocket = socket.socket () # Create the server socket
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname() # We want to bind to the same host
serverSocket.bind ((host, port)) # Connect socket to same host & port
serverSocket.listen (10) # back log

print 'Waiting for a connection'
# Time to listen for connections


while noOfConnectedDevices < DEVICE_LIMIT:
	


	print 'Iteration = ' + str(noOfConnectedDevices)
	# Accept incoming connections
	try:
		print 'Waiting for connections'
		(conn, addr) = serverSocket.accept() # Wait for a connection from the Android Phone
		print 'Accepted connection' # Connection has been established

		receivedData = conn.recv (1024)
		print 'Received Data = ' + receivedData

		if (receivedData == 'Sender'):
			print 'In IF Sender'
			noOfConnectedDevices = noOfConnectedDevices + 1
			print 'Number of Connected Devices = ' + str (noOfConnectedDevices)
			thread.start_new_thread (senderHandler, (conn,))


		elif (receivedData == 'Receiver'):
			print 'In IF Receiver'
			thread.start_new_thread (receiverHandler, (conn,))
			noOfConnectedDevices = noOfConnectedDevices + 1
			print 'Number of Connected Devices = ' + str (noOfConnectedDevices)

		else:
			conn.close()
			print 'Closed connection because it had ID = ' + receivedData

	except socket.error, msg:
		print 'Failed: Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    	#serverSocket.close()
    	
	print 'In end of try with connections = ' + str(noOfConnectedDevices) +' and device limit = ' + str (DEVICE_LIMIT)




print 'Going into an infinte loop with ' + str (noOfConnectedDevices) + ' connections'
while 1:
	pass
serverSocket.close()







