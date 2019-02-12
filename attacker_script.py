import socket
import argparse

'''
TODO:
 make the attacker script have server functionality
'''

parser = argparse.ArgumentParser()
parser.add_argument('--host',help='Host to connect to')
parser.add_argument('-p','--port',help='Port to connect or bind to')
parser.add_argument('-t','--target',help='Target ip address')
parser.add_argument('-tp','--target-port',help='Target port to check',default=None)

args = parser.parse_args()

def connect(server_ip, server_port, action, target_ip, target_port=None):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    if action == '\x01':
        portscan(client, target_ip)
    elif action == '\x02':
        portscan(client, target_ip, target_port)


def portscan(client, target_ip, target_port=None):
    if target_port:
        client.send('\x02')
        client.recv(1)
        target = '{}:{}'.format(target_ip, target_port)
        client.send(target)
    else:
        client.send('\x01')
        client.recv(1)
        client.send(target_ip)

    ports = client.recv(2048)
    open_ports = ports.split(':')
    print open_ports
    for port in open_ports:
        if port != '\x00':
            print('Port {} is open'.format(port))

def main():
    try:
        host = args.host
        port = args.port
        target = args.target
        target_port = args.target_port
    except:
        parser.print_help()
        exit(1)
    if not target_port:
        print('Doing a full port scan on: {}'.format(target))
        connect(host, int(port), '\x01', target)
    elif target_port:
        print('Checking for port: {}'.format(target_port))
        connect(host, int(port), '\x02', target, target_port)

if __name__ == '__main__':
    main()
