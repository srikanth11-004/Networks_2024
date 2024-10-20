import socket

# Create a dictionary for key-value pairs
key_value_dict = {}

# Function to handle GET request
def get(c, rec_message):
    arr = rec_message.split("=")
    key_val = arr[1].split()[0]
    if key_val in key_value_dict:
        msg = "HTTP/1.1 200 OK [value: " + key_value_dict[key_val] + "]" + "\r\n\r\n"
    else:
        msg = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
    c.send(msg.encode())

# Function to handle PUT request
def put(c, rec_message):
    arr = rec_message.split("=")
    key_value = arr[1].split("/")[0]
    value = arr[2].split()[0]
    if key_value in key_value_dict:
        key_value_dict[key_value] = value
        print(key_value_dict)
        c.send("HTTP/1.1 200 OK [Value changed for specified key]\r\n\r\n".encode())
    else:
        key_value_dict[key_value] = value
        print(key_value_dict)
        c.send("HTTP/1.1 200 OK\r\n\r\n".encode())

# Function to handle DELETE request
def delete(c, rec_message):
    arr = rec_message.split("=")
    key_val = arr[1].split()[0]
    if key_val in key_value_dict:
        key_value_dict.pop(key_val)
        msg = "HTTP/1.1 200 OK [Delete successful]\r\n\r\n"
    else:
        msg = "HTTP/1.1 404 NOT FOUND [Key element not found]\r\n\r\n"
    print(key_value_dict)
    c.send(msg.encode())

# Create a socket
dst_ip = "10.0.1.2"
s = socket.socket()
print("Socket successfully created")

# Bind socket to the destination IP and port
dport = 12346
s.bind((dst_ip, dport))
print("Socket binded to %s" % dport)

# Listen for incoming connections
s.listen(5)
print("Socket is listening")

# Map HTTP methods to corresponding functions
switch = {"PUT": put, "GET": get, "DELETE": delete}

while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    while True:
        rec_message = c.recv(1024).decode()
        print("Server received the message: " + rec_message)

        if len(rec_message) == 0:
            break

        # Determine the HTTP request type and call the corresponding function
        req = rec_message.split()[0]
        if req in switch:
            switch[req](c, rec_message)

    c.close()