# coding: utf-8

from json import load
from json import dump
from os.path import isfile
#from socket import socket
#from socket import AF_INET
#from socket import SOCK_DGRAM
#from socket import gethostbyname
#from socket import gethostname
#from socket import recvfrom
import socket
from subprocess import check_output
import threading
from time import sleep

########################################

def ping (sock, file_name):
    while True:
        data = load_conf(file_name) #$$$ Оптимизировать!!!

        for ip in data["IP"]:
#            try:
                sock.sendto("hello".encode("utf-8"), (ip, int(data["PORT"][data["IP"].index(ip)])))     #+++++++++ select.select
                data["ONLINE"][data["IP"].index(ip)] = "0"
#            except OSError:
#                online = data["ONLINE"][data["IP"].index(ip)]
#                print("123")
#                if (online == "1"):
#                    online = "0"

#                print("".format(ip, ))
#                dump_conf(file_name, data)
                sleep(1)

########################################

def listen (sock, file_name):
    turn = list()
    
    while True:
        mess, addr = sock.recvfrom(1024)
    
        rT = threading.Thread(target=filter, args=(sock, file_name, mess, addr))
        rT.start()
        turn.append(rT)
#        print(turn)

########################################

def filter (sock, file_name, mess, addr):
    data = load_conf(file_name) #$$$ Оптимизировать!!!
    mess = mess.decode("utf-8").split()
        
    if (mess[0] == "hello"):
        data["ONLINE"][data["IP"].index(mess[1])] = "1" # Временно. Нужно сделать clients в файле
        dump_conf(file_name, data)
    elif (mess[0] == "other"):
        pass

########################################

def dump_conf (file_name, data):
    with open("{}".format(file_name), 'w') as file:
        print(data)
        dump(data, file)

########################################

def init_file (file_name):
    data = {}
    data["NAME"] = list()
    data["IP"] = list()
    data["PORT"] = list()
    data["ONLINE"] = list()
    
    dump_conf (file_name, data)

########################################

def load_conf (file_name):
    with open("{}".format(file_name), 'r') as file:
        data = load(file)
        
    return data

########################################

def menu (selected_name):
    print("{1} Create new config\n"
    "{2} Use config\n"
    "{3} Delete some config\n"
    "{4} Show\n"
    "{99} Quit")
    
    com = input("{} => ".format(selected_name))
    
    return str(com)

########################################

def start_cli (file_name):
    data = load_conf(file_name)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("192.168.0.12", 0))
    sock.setblocking(True)
    
    print(check_output("ipconfig getifaddr {}".format("en0"), shell=True).decode().rstrip())
    
    return sock
    
#    print(gethostbyname(gethostname()))
#    server = ("95.73.117.213", 9002) #$$$
    
########################################

def main (file_name):
    global selected_name
    com = menu(selected_name)
    data = load_conf(file_name)

    if (com == '1'):
        name = input("[NAME]: ")
        
        print("Проверка на имя") #$$$
        
        if (not name in data["NAME"]):
            ip = input("[IP]: ")
            
            print("Проверка на ip") #$$$
        
            if (True):
                port = input("[PORT]: ")
                
                print("Проверка на оригинальность") #$$$
                
                if (True):
                    data["NAME"].append(name)
                    data["IP"].append(ip)
                    data["PORT"].append(port)
                    data["ONLINE"].append("0")
                    
                    print("Create")
        
                    dump_conf(file_name, data)
    elif (com == '2'):
        print("Load")
        selected_name = input("[NAME]: ")
    elif (com == '3'):
        print("Delete")
        name = input("[NAME]: ")
    
        if (selected_name == name):
            print("Do you want to delete the selected name?\n\t(1/Other -> Yes/No)\n")
            
            if (input(" => ") != '1'):
                return False
            
            selected_name = ""
            
        index = data["NAME"].index(name)
        data["NAME"].pop(index)
        data["IP"].pop(index)
        data["PORT"].pop(index)
        data["ONLINE"].pop(index)
        
        dump_conf(file_name, data)
    elif (com == '4'):
        print(data)
    elif (com == '99'):
        print("Exit")
        return False
    
    return True

########################################

if __name__ == '__main__':
    file_name = "/Users/sm/hack_conf.txt"
    selected_name = ""
    server = ("192.168.0.12", 9002)

    print("Проверка на существование файла") #$$$
    
    if (not isfile(file_name)):
        init_file(file_name)
        
    sock = start_cli(file_name)
    
    rT = threading.Thread(target=listen, args=(sock, file_name))
    rT.start()
    
    rT1 = threading.Thread(target=ping, args=(sock, file_name))
    rT1.start()
    
#    check_online(sock)

    try:
        while (True):
            if (not main(file_name)):
                break
    except KeyboardInterrupt:
        pass
        
    print("\nIt's All!")
    
    sock.close()
