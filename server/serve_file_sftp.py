# Copyright Trevor Chan trevchan@bu.edu
import sys
import socket
import os
import hashlib

class status:
    FOUND = 0
    BADREQUEST = 1
    TOOLARGE = 2
    NOTFOUND = 3
    PENDING = 4


# Helper function that checks if the inputted client message is valid or not
def getFilename(message):
    # Check if the request message includes a directory / (invalid)
    if ('/' in message):
        return None
    fname = None
    # Check if the request message is valid format GET fname\r\n
    if (len(message) > 5):
        if (message[0:3] == "GET" and  message[-2:] == "\r\n"):
            fname = message[4:-2]
    # Returns the filename if successful, None if unsuccessful
    return fname


# Main server function that runs the server, waits for connections, and handles responses
def server(ip):
    # Bind the receiver socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, 9000))

    # While the process is running, receive requests
    while True:
        message, ret_address = server_socket.recvfrom(1024)
        print(ret_address)
        print("Request from " + str(ret_address) + ": " +message.decode('utf-8'))
        message_status = status.BADREQUEST
        return_message = ""

        # Get the filename from the message (and check if message is invalid)
        filename = getFilename(message.decode('utf-8'))
        if (filename == None):
            return_message = "BADREQUEST\r\n"
            server_socket.sendto(bytes(return_message,'utf-8'), ret_address)
            print("Response to " + str(ret_address) + ": " + return_message)
            continue

        # Check if the file exists in the server
        if (not os.path.exists(filename)):
            return_message = "NOTFOUND " + filename + "\r\n"
            server_socket.sendto(bytes(return_message,'utf-8'), ret_address)
            print("Response to " + str(ret_address) + ": " + return_message)
            continue

        # Check if the file length is too long
        file_size = os.stat(filename).st_size
        max_length = 65507
        if (file_size > max_length):
            return_message = "TOOLARGE " + filename + "\r\n"
            server_socket.sendto(bytes(return_message,'utf-8'), ret_address)
            print("Response to " + str(ret_address) + ": " + return_message)
            continue

        # Read the file contents, get the file md5sum, and send the FOUND message is correct
        file_contents = ""
        md5 = ""
        with open(filename, 'rb') as fd:
            try:
                file_contents = fd.read()
                md5 = hashlib.md5(file_contents).hexdigest()
                return_message = ("FOUND " + filename + "\r\n" + 
                                  "MD5 0x" + md5 + "\r\n" +  
                                  "LENGTH " + str(file_size) + "\r\n" +  
                                  file_contents.decode('utf-8'))
                
                # If the return message exceeds the max length, send that it was bad
                if (len(return_message) > max_length):
                    return_message = "TOOLARGE " + filename + "\r\n"
                    server_socket.sendto(bytes(return_message,'utf-8'), ret_address)
                    print("Response to " + str(ret_address) + ": " + return_message)
                    continue

                # If everything works as intended, send the FOUND message
                server_socket.sendto(bytes(return_message,'utf-8'), ret_address)
                print("Response to " + str(ret_address) + ":\n" + 
                    "FOUND " + filename + "\r\n" + 
                    "MD5 " + md5 + "\r\n" +  
                    "LENGTH " + str(file_size) + "\r\n")

            # If the above fails for any reason, send back a BADREQUEST message 
            except:
                return_message = "BADREQUEST\r\n"
                server_socket.sendto(bytes(return_message,'utf-8'), ret_address)
                print("Response to " + str(ret_address) + ": " + return_message)
                continue


# Get the commandline arguments to see whether to use input IP or default
ip = None
if (len(sys.argv) == 1):
    ip = "127.0.0.1"
elif (len(sys.argv) > 1):
    ip = sys.argv[1]

server(ip)
