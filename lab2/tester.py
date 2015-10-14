import thread, socket, sys, time

def requester(host, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # send the request using the socket
    s.send(message+"\n")
    # recieve up to 1024 bytes from the remote server
    data = s.recv(1024)
    print(data)
    s.close()

for i in range(10):
    t = thread.start_new(requester, (sys.argv[1], int(sys.argv[2]), sys.argv[3]))

time.sleep(10)
