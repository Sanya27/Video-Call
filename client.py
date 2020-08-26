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

#HOST1 = '172.16.37.198'
#PORTA = 8000
#PORTV = 8089
#ZMQA = 'tcp://172.16.36.198:5555'

def client(HOST1,HOST2,PORT_v_recv,PORT_a_recv,PORT_v_send,PORT_a_send, ZMQA):
    b=1

    #audiosocket
    clientaudiosocket = socket.socket()
    clientaudiosocket.connect((HOST1,PORT_a_recv))
    #Audio
    chunk = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    output = True,
                    frames_per_buffer = chunk)
    #Video
    cap = cv2.VideoCapture(0)

    def receiveVideo():
        context = zmq.Context()
        footage_socket = context.socket(zmq.SUB)
        footage_socket.connect(ZMQA)
        footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        while True:
            frame = footage_socket.recv_string()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            cv2.imshow("frame",source)
            cv2.waitKey(1)
        
    def receiveAudio():
         while True:
              audioData = clientaudiosocket.recv(1024)
              stream.write(audioData)         
    Thread(target = receiveVideo).start()
    Thread(target = receiveAudio).start()

        
        #HOST_send = '192.168.0.100'
        #PORTV_send = 8085
        #PORTA_send = 8006
    b=1
    if(b==1):
        #audiosocket
        audiosocket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        audiosocket_send.bind((HOST2,PORT_a_send))
        print('audio binded')
        audiosocket_send.listen(5)
        print('audio listening')
        cAudio_send, addr = audiosocket_send.accept()
        print(addr)

        #Audio
        chunk = 1024
        chunk = 1024
        p_send = pyaudio.PyAudio()
        stream_send = p_send.open(format = pyaudio.paInt16,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = chunk)


        def recordAudio_send():
            time.sleep(5)
            while True:
                data = stream_send.read(chunk)
                if data:
                    cAudio_send.sendall(data)


        print ('Connection accepted from ', addr)

        Thread(target = recordAudio_send).start()

        time.sleep(10)
        x=input("Enter value: :")
        b=int(x)
        print(b)
    
