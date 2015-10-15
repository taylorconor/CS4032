import thread, Queue, socket, sys, os, signal

class Server(object):

    _queue = Queue.Queue()  # incoming connection queue
    _pool = []              # thread pool

    def __init__(self, host, port, threads):
        self._host = host
        self._port = port
        self._threads = threads
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # start the entire server
    def start(self):
        self._bind()
        self._createPool()
        self._listen()

    # stop the listener threads by filling the connection queue with None (which the threads will interpret as kill)
    def stop(self):
        for _ in range(self._threads):
            self._queue.put(None)

    # initialise the thread pool
    def _createPool(self):
        for i in range(self._threads):
            t = thread.start_new(self._consumer, (i,))
            self._pool.append(t)

    # bind socket to port
    def _bind(self):
        try:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self._host, self._port))  # allow connections from anywhere
        except socket.error as err:
            raise Exception("Error "+str(err[0])+", bind failed: "+err[1])

    # listen for connections
    def _listen(self):
        self._socket.listen(10)
        while True:
            conn, addr = self._socket.accept()
            self._queue.put((conn, addr), False)

    # consume an item from the queue
    def _consumer(self, cid):
        print "consumer id="+str(cid)
        waiting = True
        while waiting:
            v = self._queue.get()
            if v == None:
                break

            conn, addr = v
            res = "UNSUPPORTED"
            data = conn.recv(8096)
            if data == "KILL_SERVICE\n":
                waiting = False
                res = "STOPPING"
            elif data[:4] == "HELO":
                res = data+"IP:"+self._host+"\nPort:"+str(self._port)+"\nStudentID:f512ce082b10d3fad0900aed0845ebe073c019e15e74b8ae0878ae5fdd794f71\n"
            print("thread="+str(cid)+", data="+data)
            conn.send(res)
            conn.close()
        if not waiting:
            os.kill(os.getpid(), signal.SIGINT) # raise KeyboardInterrupt in the main thread

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python "+sys.argv[0]+" [port] [threads]"
        sys.exit()

    s = Server("0.0.0.0", int(sys.argv[1]), int(sys.argv[2]))
    try:
        s.start()
    except KeyboardInterrupt:
        s.stop()
    except Exception as e:
        print e