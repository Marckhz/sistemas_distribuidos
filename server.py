import socket
import os
from _thread import start_new_thread
#from client import CommandLineHelper
#import thread
import pickle


class Server(  ):
    
    def __init__(self,addr, port, sock=False):
        
        self.addr = addr
        self.port = port

        if sock is False:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    
    def create_connection(self):
    
        self.sock.bind((self.addr, self.port))
        self.sock.listen(1)

    def get_sockets(self):

        conn, address = self.sock.accept()
        return conn, address

    def handler(self, host):
        data = False
        struct = False
        bin_ = []
        with host[0]:
            
            while True:
                data = host[0].recv( 100000 )
                if data:
                    break
                print(data)
             #   bin_.append(data)
            struct = pickle.loads(data)
            print(struct)
            if 'ls' in struct['header']:
                self.show_files(host[0])
            elif 'mv' in struct['header']:
                self.write_file( struct )
            elif 'scp' in struct['header']:
                print(True)
                self.send_file_by_name(host, struct)
            else:
                print("do nothing")


    def write_file(self, struct):
        file_name = struct['file_name']
        with open(file_name, 'wb') as mfile:
            for i in file_name:
                mfile.write(i)

    def show_files(self, host):
        
        current_dir = os.listdir()
        elements = pickle.dumps(current_dir)
        with host:
            host.send(elements)
    

    def send_file_by_name(self, host, struct):
        current_dir = os.listdir()
        file = False
        read_data = False
        new_struct = dict()
        file_name = struct['file_name']
        print(file_name)
        if file_name not in current_dir:
            error = "el archivo no existe"
        else:
            read_data = False
            with open(file_name, 'rb') as byte_file:
                read_data = byte_file.read()
                print(read_data)
        
            new_struct['file_name'] = file_name
            new_struct['content'] = read_data

            marshall = pickle.dumps(read_data)
            with host[0]:
                try:
                    host[0].send(marshall)
                except ValueError as e:
                    print(e)
            

my_server = Server('127.0.0.1', 8322)
my_server.create_connection()
while True:
    conn = my_server.get_sockets()
    my_server.handler(conn) 
    
