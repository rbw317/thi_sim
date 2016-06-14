import sys
import zmq
import threading
import time
import common_pb2

die = False

def main():
    context = zmq.Context()
    try:
        t = threading.Thread(target=timer_thread, args=(context,))
        t.start()
    except:
        print "Error during thread initialization: ", sys.exc_info()[0]
        return

    try:
        sock = context.socket(zmq.XPUB)
        timerSubSock = context.socket(zmq.SUB)
        sock.bind("tcp://127.0.0.1:5678")
        timerSubSock.connect("tcp://127.0.0.1:5679")
        filter = "timer"
        timerSubSock.setsockopt_string(zmq.SUBSCRIBE, filter.decode('ascii'))
    except:
        print "Error during socket initialization: ", sys.exc_info()[0]
        return

    try:
        poller = zmq.Poller()
        poller.register(sock, zmq.POLLIN)
        poller.register(timerSubSock, zmq.POLLIN)
        # Run a simple "Echo" server
        while True:

            events = dict(poller.poll())
            if sock in events:
                message = sock.recv()
                if message[0] == b'\x01':
                    print "Subscription!"
                else:
                    print "Un-subscription"

            if timerSubSock in events:
                message = timerSubSock.recv()
                property = common_pb2.Property()
                property.key = "Hello"
                property.value = "World"
                print "Property: {0}, {1}".format(property.key, property.value)
                output = property.SerializeToString()
                #newProperty = property.ParseFromString(output)
                #print "New property: {0}, {1}".format(newProperty.key, newProperty.value)
                #sock.send_string(output)
                print("Serialized")
    except:
        print "Error: ", sys.exc_info()[0]
        die = True
        sock.close()
        timerSubSock.close()
        context.destroy()


def timer_thread(context):
    timerPubSock = context.socket(zmq.PUB)
    timerPubSock.bind("tcp://127.0.0.1:5679")
    while True:
        time.sleep(1)
        if die:
            return
        timerPubSock.send("timer")
        time.sleep(30000)

if __name__ == '__main__':
    main()