#!/usr/bin/python

import socket
import sys
import traceback
import os.path
import time
from threading import Thread
from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# magic numbers
SOCKET_RESPONSE_LIMIT = 1024
memory_of_nodes = {}  # a dictionary s.t. key=node and value=port
HOST = '0.0.0.0'


class Server(BaseHTTPRequestHandler):

    # This is to override the provided method
    def log_message(self, format, *args):
        return

    def response_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        if '/whisper?name=' and '&message=' in str(self.path):
            str_path = str(self.path)
            message = str_path[str_path.rfind('&'):]
            node_key = str_path[str_path.find('name='):str_path.find('&')]
            node_key[node_key.find('=')+1:]
            if node_key[node_key.find('=')+1:] not in memory_of_nodes:
                self.response_headers()
                self.wfile.write("Request cannot be fulfilled")
            else:
                self.response_headers()
                try:
                    # create a socket and send the data
                    socket_on_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_on_request.connect((memory_of_nodes[node_key[node_key.find('=')+1:]][0], memory_of_nodes[node_key[node_key.find('=')+1:]][1]))
                    socket_on_request.send("GET /" + argv[2] + "," + argv[4] + ",hello HTTP/1.1\r\n\r\n")
                    time.sleep(1)  # safety sleep
                    response = socket_on_request.recv(SOCKET_RESPONSE_LIMIT)
                except socket.error as error:
                    print(error)
                print("[" + argv[2] + "] Message sent to " + node_key[node_key.find('=')+1:] + " at " + str(memory_of_nodes[node_key[node_key.find('=')+1:]][0]) + ":" + str(memory_of_nodes[node_key[node_key.find('=')+1:]][1]) + " :: " + message[message.find('=')+1:])
        elif ',hello' in str(self.path):
            str_path = str(self.path)
            print("[" + argv[2] + "] Message received from " + str_path[str_path.find('/')+1:str_path.find(',')] + " at localhost" + ":" + str_path[str_path.find(',')+1:str_path.rfind(',')] + " :: " + str_path[str_path.rfind(',')+1:])
        else:
            self.response_headers()
            self.wfile.write("Node:" + argv[2])


def server_run(server_class=HTTPServer, server_handler=Server, port=argv[1]):
    try:
        server_address = (HOST, port)
        server_initiate = server_class(server_address, server_handler)
        server_initiate.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard Interrupt! Exiting now...")
        os.remove(os.path.join('/tmp/', argv[2]))
        print("Client name is now freed")
    except Exception:
        traceback.print_exc(file=sys.stdout)
        os.remove(os.path.join('/tmp/', argv[2]))
        print("Client name is now freed")

if __name__ == "__main__":
    # check arguments
    if not (len(argv) == 5 or len(argv) == 7) and ((argv[1] == "--name" and argv[3] == "--port") or (argv[1] == "--name" and argv[3] == "--port" and argv[5] == "--bootnodes")):
        print("Unsupported argument vector found")
        sys.exit(1)
    if os.path.isfile("/tmp/"+argv[2]):
        print("Client name is in use")
        sys.exit(2)
    else:
        # print(len(argv))
        # print(argv)
        open(os.path.join('/tmp/', argv[2]), 'a').close
        threads = []
        server_thread = Thread(target=server_run, args=(HTTPServer, Server, int(argv[4])))
        server_thread.start()
        time.sleep(1)  # safety sleep
        threads.append(server_thread)

        if len(argv) == 5:
            pass
        else:
            boot_nodes = argv[6].split(',')
            for boot_node in boot_nodes:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # client_socket.setblocking(0)
                    client_socket.connect((boot_node[:boot_node.rfind(':')], int(boot_node[boot_node.rfind(':')+1:])))
                    client_socket.send('GET / HTTP/1.1\r\n\r\n')
                    time.sleep(1)  # safety sleep
                    response = client_socket.recv(SOCKET_RESPONSE_LIMIT)
                except socket.error as error:
                    print(error)
                print("[" + argv[2] + "] Connected to " + response[response.rfind(':')+1:] + " at " + boot_node)
                memory_of_nodes[response[response.rfind(':')+1:]] = boot_node[:boot_node.rfind(':')], int(boot_node[boot_node.rfind(':')+1:])

        for thread_entry in threads:
            thread_entry.join()
else:
    sys.exit(3)
