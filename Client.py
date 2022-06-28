import tkinter as tk
from tkinter import Entry
from tkinter import *
import socket
from tkinter import filedialog
import pickle
from tkinter.messagebox import showinfo
from tkinter import messagebox
import os



IP = socket.gethostbyname(socket.gethostname())
PORT = 2728
ADDR = (IP, PORT)
SIZE = 1024
Client_DATA_PATH = "downloads_data"
# AF_INT => IPv4, SOCK_STREAM => TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

root = Tk()
root.title("Share Socket")
root.geometry("550x560+500+200")
root.configure(bg="white")
root.resizable(False,False)
image_icon =  PhotoImage(file="image/icon.png")
root.iconphoto(False, image_icon)

def select_file():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                            title='select file',
                                            filetypes=(('file_type','*.txt'),('all files','*.*')))
    
def uploder():
    with open(filename, "rb") as file:
            data = {"isfile":True, 'filesize':os.fstat(file.fileno()).st_size, 'filename':file.name, 'cmd':'UPLOAD'}
            data_pickle = pickle.dumps(data)
            client.send(data_pickle)
            ch = client.recv(1024).decode()
            if ch!= 'ok':
                client.close()
            send_data = file.read(1024)
            while True:
                client.sendall(send_data)
                send_data = file.read(1024)
                if not send_data:
                    break
            file.close()
            print('done!')
            # data = {"isfile":False,}
            # data_pickle = pickle.dumps(data)
            # client.send(data_pickle)

def downloader():
    
    filenamed =  filename1.get()
    data = {"isfile":True, 'filename':filenamed, 'cmd':'DOWNLOAD'}
    data_pickle = pickle.dumps(data)
    client.send(data_pickle)
    data = client.recv(1024)
    pickle_data = pickle.loads(data)
    client.sendall('ok'.encode())
    i = pickle_data.get('filesize')
    filepath = os.path.join(Client_DATA_PATH, filenamed)
    with open(filepath, 'wb') as f:
        data = client.recv(1024)
        f.write(data)
        si = len(data)
        while si<i:
            data =client.recv(1024)
            si += len(data)
            f.write(data)
        f.close()
        messagebox.showinfo(message=  filenamed + ' was Downloaded')


def upload():
    window = Toplevel(root)
    window.title("Upload File")
    window.geometry("550x300+500+200")
    window.configure(bg='#f4fdfe')
    window.iconphoto(False,upload_image)

    file = Button(window,text='+ Select File',command=select_file, width=15, height=5, bg='orange').place(x=200,y=50)
    
    send = Button(window,text='Send Selected File',command=uploder, width=15, height=5, bg='blue').place(x=200,y=150)

    # filename = label(text=select_file)
    window.mainloop()

def download():
    window = Toplevel(root)
    window.title("Download File")
    window.geometry("550x300+500+200")
    window.configure(bg='#f4fdfe')
    window.iconphoto(False,download_image)
    global filename1
    filename1 = Entry(window, width=20,font=('Acumin Variable Concept',18,'bold'), border=2)
    filename1.place(x=80,y=105)
    send = Button(window,text='Download File',command=downloader, width=15, height=2, bg='blue').place(x=350,y=100)
    window.mainloop()

def _list():
    window = Toplevel(root)
    window.title("List of Files")
    window.geometry("650x500+500+200")
    window.configure(bg='#f4fdfe')
    window.iconphoto(False,list_image)

    data = {"isfile":False, 'cmd':'LIST'}
    data_pickle = pickle.dumps(data)
    client.send(data_pickle)
    li = client.recv(1024).decode()
    li = li.split("\n")
    lii = ""
    for i in range(len(li)):
        lii += str(i+1) + "- "+li[i]+"\n"
    Label(window, text = lii,font=('Acumin Variable Concept',15,'bold'),bg='blue',fg='white').place(x=60,y=60)

def logout():
    client.close()
    exit(0)


Label(root, text="File Transfer with Sockets", font=('Acumin Variable Concept',20,'bold'),bg='blue',fg='white').place(x=95,y=10)
# Frame(root,width=400, height=2, bg='#f3f5f5').place(x=25,y=80)

upload_image = PhotoImage(file="Image/upload.png")
upload = Button(root, image=upload_image ,bg='#f4fdfe',bd=0, command=upload).place(x=45,y=90)

download_image = PhotoImage(file="Image/download.png")
download = Button(root, image=download_image ,bg='#f4fdfe',bd=0,command=download).place(x=290,y=90)

list_image = PhotoImage(file="Image/list.png")
list = Button(root, image=list_image ,bg='#f4fdfe',bd=0,command=_list).place(x=45,y=330)

logout_image = PhotoImage(file="Image/logout.png")
logout = Button(root, image=logout_image ,bg='#f4fdfe',bd=0,command=logout).place(x=290,y=330)


host = socket.gethostname()
Label(root, text = f'ID: {host}',bg='white',fg='black',font=('Acumin Variable Concept',15,'bold')).place(x=150,y=55)


root.mainloop()
