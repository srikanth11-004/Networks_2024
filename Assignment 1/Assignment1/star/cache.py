import socket

# Dictionary to store cache key-value pairs
cache = {}

# IP addresses and ports
cache_ip = "10.0.1.2"
server_ip = "10.0.1.3"
cache_port = 12346
server_port = 12345

# Create and configure sockets
s = socket.socket()  # Cache socket
s1 = socket.socket()  # Server socket
print("Sockets successfully created")

# Bind the cache socket to a port
s.bind((cache_ip, cache_port))
print("Cache socket binded to port %s" % cache_port)

# Connect the server socket to the server
s1.connect((server_ip, server_port))

# Cache socket starts listening for client connections
s.listen(5)
print("Cache is listening for connections...")

# Function to handle PUT requests
def put_request(parts, original_message, client_connection):
    key = parts[2].split("=")[1]
    value = parts[3].split("=")[1]

    # Forward the request to the server
    s1.send(original_message.encode())
    server_reply = s1.recv(1024).decode()

    # Check if the response is 200 OK, then cache the value
    response_status = server_reply.split()[1]
    if response_status == '200':
        cache[key] = value

    print(cache)
    client_connection.send(server_reply.encode())

# Function to handle GET requests
def get_request(parts, original_message, client_connection):
    key = parts[1].split("=")[1]

    # If the key is in the cache, send the cached value to the client
    if key in cache:
        print(cache)
        client_connection.send(('HTTP/1.1 200 OK\nvalue: ' + cache[key] + '\r\n\r\n').encode())
    else:
        # Forward the request to the server if the key is not in the cache
        s1.send(original_message.encode())
        server_reply = s1.recv(1024).decode()

        # Parse the server response and cache the value if it's 200 OK
        response_status = server_reply.split()[1]
        if response_status == '200':
            value = server_reply.split(":")[1].strip()
            cache[key] = value

        print(cache)
        client_connection.send(server_reply.encode())


# Main loop to handle incoming client requests
while True:
    client_connection, client_addr = s.accept()
    print('Connected to client at', client_addr)

    while True:
        # Receive the HTTP request from the client
        client_request = client_connection.recv(1024).decode()
        original_request = client_request

        if len(client_request) == 0:
            break

        print("\nrequest: " + client_request)

        # Clean up the request and parse it
        clean_request = client_request.replace(' ', '').replace("HTTP/1.1\r\n\r\n", '')
        request_parts = clean_request.split("/")

        # Determine the type of HTTP request and call the respective function
        if clean_request.startswith("PUT"):
            put_request(request_parts, original_request, client_connection)
        elif clean_request.startswith("GET"):
            get_request(request_parts, original_request, client_connection)
        else:
            # Send a Bad Request response for any unsupported methods
            client_connection.send('HTTP/1.1 400 BAD REQUEST\r\n\r\n'.encode())

    # Close the client connection
    client_connection.close()