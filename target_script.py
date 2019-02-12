import socket 
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--host',help='Host to connect',default=None)
parser.add_argument('-p','--port',help='Port to connect or bind to')

args = parser.parse_args()

#use as a server
def server(src_port):
    print('Binding to 127.0.0.1:{}'.format(src_port))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',src_port))
    server_socket.listen(5)
    while True:
        server_client,address = server_socket.accept()
        handle_connection(server_client)
        server_client.close()

#use a reverse connection
def connect(server_ip, server_port):
    print('Connecting to ')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip,server_port))
    handle_connection(client_socket)

def handle_connection(client):
    
    action = client.recv(1)
    #send confirmation
    client.send('\x01')
    
    #scan all ports
    if action == '\x01':
        target = client.recv(1024)
        open_ports = portscan(target)
        client.send(open_ports)
    #check specific port
    elif action == '\x02':
        target = client.recv(1024).split(':')

        test_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        port_closed = test_socket.connect_ex((target[0],int(target[1])))
        test_socket.close()

        if port_closed:
            client.send('\x00')
        else:
            client.send(target[1])

def portscan(target):
    
    open_ports = []
    for port in range(1,65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not sock.connect_ex((target,port)):
            open_ports.append(str(port))
        sock.close()
    return ':'.join(open_ports)

def main():
    try:
        host = args.host
        port = args.port
    except:
        parser.print_help()
        exit(1)
    if host:
        connect(host,int(port))
    else:
        server(int(port))

if __name__ == '__main__':
    main()
