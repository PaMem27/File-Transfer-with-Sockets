import os
import socket
import threading
import pickle
from time import process_time_ns, sleep


# get dynamic host of PC
IP = socket.gethostbyname(socket.gethostname())
PORT = 2728
ADDR = (IP, PORT)
SIZE = 1024
SERVER_DATA_PATH = "server_data"
# AF_INT => IPv4, SOCK_STREAM => TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
server.bind(ADDR)
server.listen()
print("SERVER IS UP")
    

def get_file(connection, filename, filesize):
    i = filesize
    q = 0
    li = list()  
    connection.sendall('ok'.encode())
    filename = filename.split('/')[-1]
    filepath = os.path.join(SERVER_DATA_PATH, filename)
    with open(filepath, 'wb') as f:
        data = connection.recv(1024)
        f.write(data)
        si = len(data)
        while si<filesize:
            data = connection.recv(1024)
            si += len(data)
            f.write(data)
        f.close()
        print(filename +' Received!')

def send_file(connection,filename):
    filepath = os.path.join(SERVER_DATA_PATH, filename)
    with open(filepath, "rb") as file:
        data = {"isfile":True, 'filesize':os.fstat(file.fileno()).st_size, 'filename':file.name,}
        data_pickle = pickle.dumps(data)
        connection.send(data_pickle)
        ch = connection.recv(1024).decode()
        while True:
                send_data = file.read(1024)
                if not send_data:
                    break
                connection.sendall(send_data)
        file.close()
        

def list_files(connection):
      files = os.listdir(SERVER_DATA_PATH)
      send_data = ""
      if len(files) == 0:
            send_data += "The server directory is empty"
      else:
            send_data += "\n".join(f for f in files)
      
      connection.send(send_data.encode()) 


def client_handler(connection, address):
    print(f'NEW CLIENT {address}')
    while True :
        try:
          data = connection.recv(1024)
          pickle_data = pickle.loads(data)
       
          if pickle_data.get('isfile') and pickle_data.get('cmd')=='UPLOAD':
            get_file(connection, pickle_data.get('filename'), pickle_data.get('filesize'))

          elif pickle_data.get('isfile') and pickle_data.get('cmd')=='DOWNLOAD':
            send_file(connection, pickle_data.get('filename'))
            
          elif pickle_data.get('isfile')==False and pickle_data.get('cmd')=='LIST':
              list_files(connection)

          elif pickle_data.get('isfile')==False and pickle_data.get('cmd')=='LOGOUT':
                break
          else:
            sleep(3)
            continue
        except:
          sleep(3)
          continue
       

    connection.close()
       


while True:
    connection, address = server.accept()
    thread = threading.Thread(target=client_handler,kwargs={'connection':connection,'address' :address})
    thread.start()
