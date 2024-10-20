import socket
import time

# Server IP and Port
serverIP = "10.0.1.2"
port = 12346

# Create socket and connect to server
s = socket.socket()
s.connect((serverIP, port))

# Function to handle GET request
def get():
    key_value = raw_input("Key: ")
    return 'GET /assignment1?key=' + key_value + ' HTTP/1.1\r\n\r\n'

# Function to handle PUT request
def put():
    key_value = raw_input("Key: ")
    value = raw_input("Value: ")
    return 'PUT /assignment1/key=' + key_value + '/value=' + value + ' HTTP/1.1\r\n\r\n'

# Function to handle DELETE request
def delete():
    key_value = raw_input("Key: ")
    return 'DELETE /assignment1/key=' + key_value + ' HTTP/1.1\r\n\r\n'

# Map HTTP request types to corresponding functions
mapping = {
    'G': get,
    'P': put,
    'D': delete
}

while True:
    # Menu for HTTP request types
    print("\n-------------------------------------")
    print("Please enter the HTTP request type:")
    print("G-GET\nP-PUT\nD-DELETE\nE-exit\n")
    r = raw_input()

    if r == 'E':  # Exit if the user chooses 'E'
        break
    elif r in mapping:
        # Generate the request and send it to the server
        request = mapping[r]()
        s.send(request.encode())

        # Measure the response time
        start_time = time.time()
        response = s.recv(1024)
        elapsed_time = round(time.time() - start_time, 5)

        # Print the response and time taken
        print('\r\n\r\nTime: %s seconds\r\n' % elapsed_time + 'Client received: ' + response.decode())
    else:
        print("Invalid request type! Please choose among G, P, D, and E request types.")
        continue

# Close the connection
s.close()