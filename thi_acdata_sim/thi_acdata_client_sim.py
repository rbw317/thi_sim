import zmq
import sys
import common_pb2

def main():
    try:
        context = zmq.Context()

        # Define the socket using the "Context"
        sock = context.socket(zmq.SUB)
        sock.connect("tcp://127.0.0.1:5678")
        sock.setsockopt(zmq.SUBSCRIBE, b"")
    except:
        print "Error during initialization: ", sys.exc_info()[0]
        return

    try:
        input = sock.recv_string()
        property = common_pb2.Property.ParseFromString(input)
    except:
        print "Error: ", sys.exc_info()[0]
        sock.close()
        context.destroy()


if __name__ == '__main__':
    main()