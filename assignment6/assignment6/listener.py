import zmq
import threading

def retrieve_weather_data(latitude, longitude, callback=None):
    """
    Takes latitude, longitude and a callback function to retrieve weather data from the ZMQ server
    In turn, a callback function is used to handle returning the data
    """
    # Create ZeroMQ context
    context = zmq.Context()

    # Create REQ socket and connect to the server
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://localhost:5555")

    # Send location data as JSON
    location_data = {"latitude": latitude, "longitude": longitude}
    req_socket.send_json(location_data)

    # Receive acknowledgment
    ack = req_socket.recv()

    # Subscribe to response "feed" asynchronously
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5556")
    sub_socket.subscribe(b"")


    # nonlocal to handle the ansychronous processing
    weather_data = None

    # Define response function
    def response_handler():
        nonlocal weather_data
        while True:
            response = sub_socket.recv_json()
            if callback:
                callback(response)

    # Start response handler thread
    threading.Thread(target=response_handler, daemon=True).start()



