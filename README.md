# Server and Client File Transfer
System for running a server (default on 127.0.0.1:9000) that receives SFTP requests from clients, searches for files on the server, then responds with response code along with the file contents, md5 sum, and file length if successful.

Clients send a request to the server for the file of input name. If successful, prints nothing and creates the file on the client system. If unsuccessful, prints out error message (such as badrequest, file toolarge, etc.)