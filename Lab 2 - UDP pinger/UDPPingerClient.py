import time
import sys
import socket

cliArguments = sys.argv

timeout = 1 # second(s)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(timeout)
hostList = cliArguments[1].split(":")
host = str(hostList[0])
port = int(hostList[1])

pingCount = 0

while pingCount < 10: 
	pingCount += 1
	pingMsg = "Ping " + str(pingCount) + " " + str(time.time())
    
	try:	
		clientSocket.sendto(pingMsg.encode(),(host, port))
		response, address = clientSocket.recvfrom(1024)
		response = str(response)[2:-1]
		timeDiff = time.time()-float(str(response).split(" ")[2])
		truncatedTimeDiff = float("{0:.5f}".format(timeDiff))
		print("Response received from " + str(address) + " in " + str(truncatedTimeDiff) +" seconds: \n" + str(response))
		
	except socket.timeout:
		print("Request timed out.")
		continue

clientSocket.close()