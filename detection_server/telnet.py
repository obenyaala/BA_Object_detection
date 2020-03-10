# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:53:50 2020

@author: WN00151959
"""


import telnetlib
import os
import socket
import _thread
import detection
import calibration
import time

HOST = "192.168.0.4"
user = "admin"+os.linesep
leave = False
FTPIMAGES = "D:/Desktop/BA/ftpImages"


def take_picture():
    print("take a picture!")
    tn = telnetlib.Telnet(HOST)
    tn.read_until("User:".encode())
    tn.write(user.encode())
    tn.read_until("Password:".encode())
    tn.write(os.linesep.encode())
    tn.read_until("User Logged In".encode())
    cmd = "SE8"+os.linesep
    tn.write(cmd.encode())
    tn.close()
    
def get_image():
    while True:
        for files in os.listdir(FTPIMAGES):
            if files.endswith(".jpg"):
                return os.path.join(FTPIMAGES, files)

def start_sending(c, cl):
    print("accepted a client on port 23")
    login = False
    
    # Receive data from client
    c.sendall(("Welcome to In-Sight(tm)  9912M Session 0"+os.linesep).encode())
    c.sendall(("User:"+os.linesep).encode())
    cmd = ""
    breaker = ""
    while True:     
        data = c.recv(128)
        line = data.decode('UTF-8')    # convert to string (Python 3 only)
        breaker = breaker + data.decode('UTF-8')
        line = line.replace(os.linesep, "")
        if data == "".encode():
            pass
            #print("exit the connection")
            #break
        elif data == os.linesep.encode() or data.endswith(os.linesep.encode()) or breaker == os.linesep:
            if data.endswith(os.linesep.encode()) and len(line) > 0:
                cmd = line
            print("cmd:",cmd)
            if cmd == "exit":
                print("exit the connection")
                break
            elif cmd == "admin":
                login = True
                c.sendall(("Password:"+os.linesep).encode())
            elif cmd == "" and login:
                print("password entered!")
                c.sendall(("User Logged In"+os.linesep).encode())
                login = False
            elif cmd == "GO":
                c.sendall(("1"+os.linesep).encode())
            elif cmd == "GJ":
                c.sendall(("1"+os.linesep).encode())
                c.sendall(("31"+os.linesep).encode())
            elif cmd == "SW8":
                print("run detection: ")
                time.sleep(0.2)
                c.sendall(("1"+os.linesep).encode())
                take_picture()
                """
                for clts in map_connection_client:
                    if clts[0][0] == cl[0]:
                        clts[1].sendall(("(1.000)(1)(1)(-954)(154)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)"+os.linesep).encode())
                """
                path = get_image()
                time.sleep(0.3)
                print("Image path:",path)
                detected_point = detection.get_detection(path)
                if detected_point != (-1,-1):
                    calib_point = calibration.get_Cordinates(detected_point)
                    print("(",int(calib_point[0]),",",int(calib_point[1]),")")
                    
                    
                    for clts in map_connection_client:
                        if clts[0][0] == cl[0]:
                            clts[1].sendall(("(1.000)(1)(1)("+str(int(calib_point[0])-15)+")("+str(int(calib_point[1])+12)+")(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)(0)"+os.linesep).encode())
                    
                
            cmd = ""
        elif str(data) == "b'\\r'":
            breaker = data.decode('UTF-8')
        else:
            cmd = cmd + line

def send_server_info(sock_listen):
    global map_connection_client
    map_connection_client = []
    while True:
        print("waiting for client on port 3000")
        connection_send, client = sock_listen.accept()
        for clts in map_connection_client:
            print("test if there:",clts[0][0],client[0],clts[0][0] == client[0])
            if clts[0][0] == client[0]:
                map_connection_client.remove(clts)
        map_connection_client.append((client, connection_send))
        print("accepted a client on port 3000")
    
def start_server():
    print("starting server . . . ")
    SERVER = '192.168.0.1'
    PORT = 23
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = (SERVER, PORT)
    sock.bind(server_address)
    # Listen for incoming connections
    #Listen on port 3000
    sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_listen.bind(("192.168.0.1",3000))
    sock_listen.listen(1)
    sock.listen(0)
    _thread.start_new_thread(send_server_info, (sock_listen,))
    
    while True:
        print("waiting for connection on Port 23")
        connection, client_address = sock.accept()
        _thread.start_new_thread(start_sending, (connection,client_address,))


start_server()   
