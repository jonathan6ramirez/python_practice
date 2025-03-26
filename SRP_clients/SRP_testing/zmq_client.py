import zmq

# Set up ZeroMQ context
context = zmq.Context()
socket = context.socket(zmq.SUB)  # SUB = Subscriber mode
socket.connect("tcp://192.168.1.100:5555")  # Change to server IP if needed
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

print("Listening for alerts...")

while True:
    message = socket.recv_string()
    print(f"🚨 {message}")  # Display alert in real-time
