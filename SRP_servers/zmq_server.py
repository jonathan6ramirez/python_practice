import zmq
import time

# Set up ZeroMQ context
context = zmq.Context()
socket = context.socket(zmq.PUB)  # PUB = Publisher mode
socket.bind("tcp://*:8000")  # Listen on port 5555


def send_alert(alert_name):
    """Sends an alert to all subscribers."""
    message = f"ALERT: {alert_name}"
    print(f"Sending alert: {message}")
    socket.send_string(message)


if __name__ == "__main__":
    while True:
        user_input = input("Enter an alert (or 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            break
        send_alert(user_input)
