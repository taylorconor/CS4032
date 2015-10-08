import threading, Queue, socket, sys

class Server(object):

    _queue = Queue.Queue()  # connection queue
    _pool = []              # thread pool

    def __init__(self, port, threads):
        self._port = port
        self._threads = threads
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # start the entire server
    def start(self):
        self._bind()
        self._createPool()
        self._listen()

    # stop the listener threads
    def stop(self):
        for i in range(self._threads):
            self._pool[i].terminate()

    # initialise the thread pool
    def _createPool(self):
        for i in range(self._threads):
            thread = threading.Thread(target=self._consumer, args=(i,))
            thread.start()
            self._pool.append(thread)

    # listen for connections
    def _listen(self):
        self._socket.listen(10)
        while True:
            conn, addr = self._socket.accept()
            self._queue.put((conn, addr), False)

    # bind socket to port
    def _bind(self):
        try:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # allow connections from anywhere
            self._socket.bind(("0.0.0.0", self._port))
        except socket.error as err:
            raise Exception("Error "+str(err[0])+", bind failed: "+err[1])

    # consume an item from the queue
    def _consumer(self, cid):
        print "consumer id="+str(cid)
        while True:
            conn, addr = self._queue.get()
            print "Consumer "+str(cid)+"recieved connection from "+addr[0]+":"+str(addr[1])
            data = conn.recv(8096)
            print "id="+str(cid)+"data = "+data
            conn.send("<pre>Hello, "+addr[0]+":"+str(addr[1])+"\n\n"+data+"</pre>")
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python "+sys.argv[0]+" [port] [threads]"
        sys.exit()

    s = Server(int(sys.argv[1]), int(sys.argv[2]))
    try:
        s.start()
    except (KeyboardInterrupt):
        s.stop()
    except Exception as e:
        print e