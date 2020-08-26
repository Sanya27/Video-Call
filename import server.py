import server

HOST1 = '172.16.37.198'
HOST2 = '172.16.37.141'
PORT_v_send = 8089
PORT_a_send = 8000
PORT_v_recv = 8085
PORT_a_recv = 8006
ZMQA = 'tcp://172.16.37.198:5555'
ZMQAA = 'tcp://172.16.37.141:5554'

server.server(HOST1, HOST2, PORT_v_send, PORT_a_send, PORT_v_recv, PORT_a_recv,ZMQA,ZMQAA)       

