import socket
import mimetypes

# Server config
serverAddress = "127.0.0.1" # socket.gethostname()
serverPort = 4471
maxConnections = 1

# Start server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(maxConnections)
	
def sendHeader(code, mimeType):
	mimeType = str(mimeType)
	print("Sending header for status code " + str(code))
	if code is 200:
		connectionSocket.send(str("HTTP/1.1 200 OK\r\nContent-Type: " + mimeType + "; charset=UTF-8\r\n\r\n").encode())
	elif code is 404:
		connectionSocket.send(str("HTTP/1.1 404 NOT FOUND\r\nContent-Type: " + mimeType + "; charset=UTF-8\r\n\r\n").encode())
	elif code is 500:
		connectionSocket.send(str("HTTP/1.1 500 INTERNAL SERVER ERROR\r\nContent-Type: " + mimeType + "; charset=UTF-8\r\n\r\n").encode())

def sendFile(filePath, header):
	filePath = str(filePath)
	if "b'" in filePath:
		filePath = filePath[2:-1]
	f = open(filePath,'rb')
	print("File " + filePath + " opened")
	outputData = f.read(1024)
	fileMimeType = mimetypes.guess_type(filePath, strict=True)[0];
	print("File MIME type: " + fileMimeType)
	sendHeader(header, fileMimeType)
	while (outputData):
		connectionSocket.send(outputData)
		outputData = f.read(1024)
	print("File " + filePath + " sent")
	f.close()

while True:
	"Server request handling loop"
	
	print("HTTP server ready on "+str(serverAddress) + " at port "+str(serverPort))
	connectionSocket, addr = serverSocket.accept()

	try:
		message =  connectionSocket.recv(1024)
		filePath = message.split()[1]
		print("File requested by client " + str(addr) + ": " + str(filePath)[2:-1])
		if str(filePath)[2:-1] is "/":
			sendFile("index.html", 200)
		else: 
			sendFile(filePath[1:], 200)
		connectionSocket.close() 

	except IOError:
		# Can't find/open that, send a 404
		print("Unable to open/read file " + str(filePath))
		sendHeader(404, "text/html")
		if ".html" in str(filePath):
			sendFile("404.html", 0)
		connectionSocket.close()
		
	except:
		# Server is bork, send a 500
		print("Unhandled server error")
		sendHeader(500, "text/html")
		if ".html" in str(filePath):
			sendFile("500.html", 0)
		connectionSocket.close()

serverSocket.close()