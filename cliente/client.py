import socket
import shutil
import argparse
import pickle


class CommandLineHelper():


    parser = argparse.ArgumentParser(description="Simple Interface for some common \
                                                     UNIX comamnds"
                                                     )
    parser.add_argument('-mv',"--Move",dest="File",
                                help="move files, just like UNIX system" )
    
    parser.add_argument('-ls', '--Ls',  help="Show a list of files of the current dir")
    

    parser.add_argument('-scp', "--SCP", dest="SCP", help="Download the file from remote")

    argument = parser.parse_args()




class Client():

    def __init__(self,addr, port, sock=False):

        self.addr = addr
        self.port = port
        if sock is False:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_server(self):
        
        host = self.sock.connect((self.addr, self.port))
        return host

    def send_mssg(self):
        self.get_server()
        struct = dict()
        struct['header']  ='ls'
        data = pickle.dumps(struct)

        self.sock.send(data)
 
        print(self.return_msg() )


    def return_msg(self):
        
        data = self.sock.recv(1000000) 
        message = pickle.loads(data)
   
        return message

    def send_file(self, file):
        self.get_server()
        #command = self.sock.send('mv')
    
        struct = dict()
        struct['header'] = 'mv'
        this_file = False
        byte_arr = []
        print("-->", file)
        with open(file, 'rb') as bit_file:
            this_file = bit_file.read()
            byte_arr.append(byte_arr)
        print(byte_arr)
        struct['file_name'] = b"".join( byte_arr )
        
        
        bin_ = pickle.dumps(struct)

        data = self.sock.send(bin_)
        print(data)
        print("archivo enviadoooo")
    
    def download_file(self, file_name):
        self.get_server()
        struct = dict()
        struct['header'] = 'scp'
        struct['file_name'] = file_name
        
        as_json = pickle.dumps(struct)
        
        if as_json:
            self.sock.send(as_json)

        data = False 
        packets = []
        while True:
            data = self.sock.recv(1000000) 
            if not data:
                break
            packets.append(data)
            print("--> ", data)
        print(packets) 
        new_struct = pickle.loads(b"".join(packets) )
        
        print('///',new_struct)
        with open(file_name, 'wb') as d_file:
            d_file.write(new_struct)

if __name__=="__main__":
    command_line = CommandLineHelper()
    client = Client('127.0.0.1', 8322)
    if command_line.argument.File:
            client.send_file(command_line.argument.File)
    if command_line.argument.Ls:
        client.send_mssg()
    if command_line.argument.SCP:
        client.download_file(command_line.argument.SCP)

