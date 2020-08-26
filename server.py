import cv2
import numpy as np
import socket
import sys
import zmq
import pickle
import base64
import struct
import pyaudio
import threading
from threading import Thread
import time

def server(HOST1,HOST2,PORT_v_send,PORT_a_send, PORT_v_recv, PORT_a_recv,ZMQA):
      
#HOST1 = '192.168.0.107'
#PORT_v_send = 8089
#PORT_a_send = 8000
    #ZMQA = 'tcp://172.16.37.198:5555'
    #videosocket
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.bind(ZMQA)
    #audiosocket
    audiosocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audiosocket.bind((HOST1,PORT_a_send))
    print('audio binded')
    audiosocket.listen(5)
    print('audio listening')
    cAudio, addr = audiosocket.accept()
    print(addr)
    #Video
    cap = cv2.VideoCapture(0)
    #Audio
    chunk = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk)


    def recordVideo():
        while True:
            grabbed, frame = cap.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)
            print("sending data")

    def recordAudio():
        time.sleep(5)
        while True:
            data = stream.read(chunk)
            if data:
                cAudio.sendall(data)

    print ('Connection accepted from ', addr)

    Thread(target = recordAudio).start()
    Thread(target = recordVideo).start()
    i=0
    b=1
    while(i<1):
        try:
            if(b==1):
                #HOST2 = '172.16.37.141'
                #PORT_a_recv = 8006
                #PORT_v_recv = 8085

                #audiosocket
                clientaudiosocket_recv = socket.socket()
                clientaudiosocket_recv.connect((HOST2,PORT_a_recv))
                i=1
                #Audio
                chunk = 1024
                p_recv = pyaudio.PyAudio()
                stream_recv = p_recv.open(format = pyaudio.paInt16,
                                channels = 1,
                                rate = 44100,
                                output = True,
                                frames_per_buffer = chunk)


                def receiveAudio_recv():
                    while True:
                          audioData_recv = clientaudiosocket_recv.recv(1024)
                          stream_recv.write(audioData_recv)
                          if(b==0):
                              print("kill thread")
                              break

                Thread(target = receiveAudio_recv).start()
                time.sleep(10)
        
                x=input("Enter value: ")
                b=int(x)
                print(b)
            
        except:
            pass

 #server('172.16.37.198','172.16.37.141',8089,8000,8085,8006,'tcp://172.16.36.121:5555)
