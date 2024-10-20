import socket

# Dictionary to store key-value pairs
data = {}

# Server IP and port configuration
dst_ip = "10.0.1.3"

s = socket.socket()
print("Socket successfully created")

dport = 12345

s.bind((dst_ip, dport))
print("Socket binded to %s" % (dport))

s.listen(5)
print("Socket is listening")


# Function to handle PUT requests
def put(c, request_message):
    # Clean up the request message
    request_message = request_message.replace(" HTTP/1.1\r\n\r\n", '')
    request_message = request_message.replace(" ", '')

    # Split the request message to extract key and value
    split_message = request_message.split("=")

    value = split_message[2]
    key = split_message[1].split("/")[0]

    # Handle the PUT logic
    if key in data:
        print('NOTE: Entered key is already present!\n')
        c.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
        data[key] = value
        print(data)
    else:
        data[key] = value
        print(data)
        c.send('HTTP/1.1 201 Created\r\n\r\n'.encode())


# Function to handle GET requests
def get(c, request_message):
    # Clean up the request message
    request_message = request_message.replace(" HTTP/1.1\r\n\r\n", '')
    request_message = request_message.replace(" ", '')

    # Split the request message to extract the key
    split_message = request_message.split("=")
    key = split_message[1]

    # Handle the GET logic
    if key in data:
        response_message = 'HTTP/1.1 200 OK \nValue: ' + data[key]
    else:
        response_message = 'HTTP/1.1 404 Value NOT FOUND\r\n\r\n'

    print(data)
    c.send(response_message.encode())

# Dictionary to map request methods to their corresponding functions
request_handlers = {
    "PUT": put,
    "GET": get
}


# Main loop for accepting client connections
while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    while True:
        request_message = c.recv(1024).decode()
        if len(request_message) == 0:
            break

        print("Server received the message: " + request_message)

        # Identify the request type (PUT, GET, DELETE) and call the corresponding function
        request_type = request_message.split()[0]
        if request_type in request_handlers:
            request_handlers[request_type](c, request_message)  # Call the appropriate function
        else:
            print(data)
            c.send('HTTP/1.1 400 BAD REQUEST\r\n\r\n'.encode())

    c.close()