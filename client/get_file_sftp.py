# Copyright Trevor Chan trevchan@bu.edu
import sys
import socket
import hashlib

# Main client function that sends the message
def client(file, ip):
    # Bind the socket, send the get request, then wait for the response
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set up the message and send it to the ip address on port 9000
    message = "GET " + file + "\r\n"
    client_socket.sendto(bytes(message,'utf-8'), (ip, 9000))

    # Wait for the reply from the server
    reply = client_socket.recv(65507)

    # Iterate through the message contents
    message_contents = reply.decode('utf-8').split('\r\n')
    return_code = message_contents[0].split()[0]
    filename = message_contents[0].split()[1]

    # Check if the return codes were bad
    if (return_code == "BADREQUEST"):
        print("Error: Bad Request")
        exit(0)
    
    # Check if the file was not found
    if (return_code == "NOTFOUND"):
        print("Error: File not found")
        exit(0)
    
    # Check if the length was too long
    if (return_code == "TOOLARGE"):
        print("Error: File too large")
        exit(0)
    
    # If file was found, create the file (or overwrite)
    if (return_code == "FOUND"):

        # Check if the MD5sum is mismatched
        md5 = message_contents[1].split()[1]
        file_contents = message_contents[3]
        if (md5 != hashlib.md5(file_contents.encode()).hexdigest()):
            print("Error: MD5 mismatch")
            exit(0)
        
        # Create the file
        with open(filename, 'w') as f:
            f.write(file_contents)
            f.close()

# Get the commandline arguments to see whether to use input IP or default
ip = None
if (len(sys.argv) == 1):
    print("Error: No file specified")
    exit(1)
elif (len(sys.argv) > 2):
    ip = sys.argv[2]
else:
    ip = "127.0.0.1"

client(sys.argv[1], ip)
    