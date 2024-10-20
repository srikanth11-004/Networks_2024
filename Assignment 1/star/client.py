import socket
import time

# Server IP and Port
serverIP = "10.0.1.2"
dst_ip = "10.0.1.2"
s = socket.socket()
port = 12346
s.connect((dst_ip, port))

# Function to handle GET request
def get():
    key_value = raw_input("Key: ")
    return 'GET /assignment1?key=' + key_value + ' HTTP/1.1\r\n\r\n'

# Function to handle PUT request
def put():
    key_value, value = raw_input("Key: "), raw_input("Value: ")
    return 'PUT /assignment1/key=' + key_value + '/value=' + value + ' HTTP/1.1\r\n\r\n'

# Map HTTP request types to the corresponding functions
switch = {
    'G': get,
    'P': put
}

while True:
    # Menu for HTTP request types
    print("\r\n\r\n---------------------------------")
    print("Please enter the HTTP request type")
    print("\nG-GET\nP-PUT\nE-exit\n")
    r = raw_input()

    if r == 'E':  # Exit if the user chooses 'E'
        break
    elif r in switch:
        # Generate the request and send it to the server
        request = switch[r]()
        s.send(request.encode())

        # Measure the response time
        start_time = time.time()
        response = s.recv(1024)
        elapsed_time = round(time.time() - start_time, 5)

        # The response and time taken
        print('\r\n\r\nTime: %s seconds\r\n' % elapsed_time + '\n\nClient received: ' + response.decode())
    else:
        print("Invalid HTTP request type! Please choose among G, P or E.")
        continue

# Close the connection
s.close()