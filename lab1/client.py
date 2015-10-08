import sys
import socket

def getResponse(host, port, message):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	s.send("GET /echo.php?message="+message+" HTTP/1.1\r\n\r\n");
	data = s.recv(1024)
	s.close()
	return data
	
if len(sys.argv) != 4:
	print "Usage: python "+sys.argv[0]+" [host] [port] [message]\n"
else:
	print getResponse(sys.argv[1], int(sys.argv[2]), sys.argv[3])+"\n"