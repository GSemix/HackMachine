# coding: utf-8

from json import dump
from json import load
from os.path import isfile
from subprocess import check_output
import datetime
from abc import ABC
from abc import abstractmethod
from time import sleep
import socket
import http.client
from hashlib import md5
import threading
from sys import exit

class File (ABC):

    path_files = "/Users/sm/Desktop/Projects/My/HackMachine/Logs/"

    def __init__ (self, file_name):
        self.file_name = self.path_files + str(file_name)
        
        if (not isfile(self.file_name)):
            self.data = self.start_file()
            print("[+] File {} ".format(self.file_name))
        else:
            self.data = self.load_conf()

    @abstractmethod
    def load_conf (self):
        pass

    @abstractmethod
    def start_file (self):
        pass
     
    @abstractmethod
    def __del__ (self):
        pass
    
class Json (File):

    def dump_conf (self):
        with open("{}".format(self.file_name), 'w') as file:
            dump(self.data, file)
                        
    def load_conf (self):
        with open("{}".format(self.file_name), 'r') as file:
            return load(file)
    
    def start_file (self):
        self.data = {}
        self.data["NAME"] = list()
        self.data["IP"] = list()
        self.data["PORT"] = list()
        self.data["ONLINE"] = list()
        
        self.dump_conf()
        
        return self.data
        
    def __del__ (self):
        self.dump_conf()
    
class Txt (File):

    def dump_conf (self):
        with open("{}".format(self.file_name), 'a') as file:
            file.write(self.data + "\n")
                        
    def load_conf (self):
        with open("{}".format(self.file_name), 'r') as file:
            try:
                last = file.readlines()[-1]
                if (last.split()[1] == "STOPED"):
                    last = ' '.join(last.split()[3:-1])
                else:
                    raise
            except:
                self.data = "\n\n###-> STOPED in ?-?-? ?:? <-###\n"
                self.dump_conf()
                last = None
            
            Date = datetime.datetime.now()
            self.data = "\n\n###-> STARTED in " + Date.strftime("%d-%m-%Y %H:%M") + " <-###\n" #       Сделать Функцию в File для получения даты и времени
            self.dump_conf()
            
        return last
    
    def start_file (self):
        Date = datetime.datetime.now()
    
        with open("{}".format(self.file_name), 'w') as file:
            file.write("###-> STARTED in " + Date.strftime("%d-%m-%Y %H:%M") + " <-###\n\n")
        
        return "START"
    
    def __del__ (self):
        print("44444444444444")
        Date = datetime.datetime.now()
        self.data = "\n###-> STOPED in " + Date.strftime("%d-%m-%Y %H:%M") + " <-###"
    
        self.dump_conf()
        
class _Cli ():
    
    def __init__ (self, Clients, Logs):
        try:
            self.sock = self.start_cli()
            Logs.data = "[+] Client started in {} ({})".format(self.get_local_ip_addr(), self.get_global_ip_addr())
        except:
            Logs.data = "[-] Client didn't start!"
            
        Logs.dump_conf()
        
    def start_cli (self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.get_local_ip_addr(), 0))
        s.setblocking(True)
    
        return s
        
    def send_mess (self, mess, name, Clients, Logs):
        try:
            _index = Clients.data["NAME"].index(name)
            self.sock.sendto("{}".format(mess).encode("utf-8"), (Clients.data["IP"][_index], int(Clients.data["PORT"][_index])))
            Logs.data = "[+] Message ({}) to {}@{}:{} successfully sent".format(mess, name, Clients.data["IP"][_index], Clients.data["PORT"][_index])
            Logs.dump_conf()
            
            return "OK"
        except:
            Logs.data = "[-] Error! Message ({}) to {}@{}:{} not sent!".format(mess, name, Clients.data["IP"][_index], Clients.data["PORT"][_index])
            Logs.dump_conf()
            
            return "NO"
        
    def listen (self, Logs, Clients, online_servers):
        global end
        
        Logs.data = "Listen started"
        Logs.dump_conf()
    
        while end:
            mess, addr = self.sock.recvfrom(1024)
            mess = mess.decode("utf-8")
            
            _profile = who_is_it(online_servers, Clients, mess.split()[0], addr)
            
            if (_profile != None):
                Logs.data = "[+] Received message ({}) from {}@{}:{}".format(mess, _profile.name, _profile.ip, _profile.port)
                Logs.dump_conf()
                
                mess = mess.split()
            
                if (mess[1] == "Encrypted_Key"):
                        pass
                        
        Logs.data = "Listen stoped!"
        Logs.dump_conf()
        print("0000000000000")
                
        exit(0)
        
    def get_global_ip_addr (self):
        try:
            conn = http.client.HTTPConnection("ifconfig.me")
            conn.request("GET", "/ip")
            
            return conn.getresponse().read().decode()
        except:
            return None

    def get_local_ip_addr (self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
            
        return ip
        
    def __del__ (self):
        self.sock.close()
        
class Profiles ():
    
    def __init__ (self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        
########################################

def HashMD5(words):
    return md5(words.encode("utf-8")).hexdigest()
    
def DeCrypt(messageEnCrypt):
    messageEnCrypt = list(messageEnCrypt)
    messageDeCrypt = ''
    messageHesh = ''
    long = len(messageEnCrypt) - 32

    if len(messageEnCrypt) < 64: # было до 63
        for x in range(0, long*2, 2):
            messageHesh += messageEnCrypt[x + 1]
            messageEnCrypt[x + 1] = " "
        for x in range(long*2, len(messageEnCrypt), 1):
            messageHesh += messageEnCrypt[x]
            messageEnCrypt[x] = " "
        for x in range(0, len(messageEnCrypt), 1):
            if messageEnCrypt[x] == " ":
                messageEnCrypt[x] = ""

    else:
        for x in range(0, 64, 2):
            messageHesh += messageEnCrypt[x + 1]
            messageEnCrypt[x + 1] = " "
        for x in range(0, 64, 2):
            messageEnCrypt[x + 1] = ""

    messageEnCrypt = "".join(messageEnCrypt)
    messageDeCrypt = ""
    k = 0
    
    for x in messageEnCrypt:
        messageDeCrypt += chr(ord(x) - ord(messageHesh[k]))
        if k == 31:
            k = 0
        else:
            k += 1
            
    return messageDeCrypt

def who_is_it (online_servers, Clients, mess, addr):
    for profile in online_servers:
        if ((profile.ip, int(profile.port)) == addr):
            return profile
    
    if (len(mess) >= 33):
        if (DeCrypt(mess) in Clients.data["NAME"]):
            _index = Clients.data["NAME"].index(DeCrypt(mess))
            _profile = Profiles(Clients.data["NAME"][_index], Clients.data["IP"][_index], Clients.data["PORT"][_index])
            online_servers.append(_profile)
            
            return _profile

    return None

def ping (Clients, Cli, Logs, online_servers):
    global end
    
    Logs.data = "Ping started"
    Logs.dump_conf()
    
    while end:
        for name in Clients.data["NAME"]:
            Cli.send_mess("hello", name, Clients, Logs)
        sleep(10)
            
        for serv in online_servers:
            del(serv)
            online_servers = list()
            
    Logs.data = "Ping stoped!"
    Logs.dump_conf()
    print("0000000000000")
    
    exit(0)

def main (online_servers, procs, end):
    Clients = Json("clients.json")
    Logs = Txt("logs.txt")
    
    if (Logs.data == None):
        print("\n[-] The work was completed incorrectly!", end = "\n")
    elif (Logs.data == "START"):
        pass
    else:
        print("\nThe work has been completed in " + Logs.data, end = "\n")
        
    Cli = _Cli(Clients, Logs)
    
    _listen = threading.Thread(target = Cli.listen, args = (Logs, Clients, online_servers))
    procs.append(_listen)
    _listen.daemon = True
    _listen.start()
    
    _ping = threading.Thread(target = ping, args = (Clients, Cli, Logs, online_servers))
    procs.append(_ping)
    _ping.daemon = True
    _ping.start()
    
    try:
        while (True):
            if (not menu_profile(Clients, Logs, online_servers)):
                break
    except KeyboardInterrupt:
        pass

    del(Clients)
    
    try:
        del(Cli)
        Logs.data = "Client stoped!"
        Logs.dump_conf()
    except AttributeError:
            pass

    return Logs
    
def menu_profile (Clients, Logs, online_servers):
    global selected_name
    
    print("\n{1} Create new config\n"
    "{2} Use config\n"
    "{3} Delete some config\n"
    "{4} Show\n"
    "{99} Quit\n")
    
    com = input("{} => ".format(selected_name))
    
    if (com == '1'):
        name = input("[NAME]: ")
        
        print("Проверка на имя") #$$$
        
        if (not name in Clients.data["NAME"]):
            ip = input("[IP]: ")
            
            print("Проверка на ip") #$$$
        
            if (True):
                port = input("[PORT]: ")
                
                print("Проверка на оригинальность") #$$$
                
                if (True):
                    Clients.data["NAME"].append(name)
                    Clients.data["IP"].append(ip)
                    Clients.data["PORT"].append(port)
                    Clients.data["ONLINE"].append("0")
                    
                    Logs.data = "[+] Create new PROFILE: {}@{}:{}".format(name, ip, port)
                    Logs.dump_conf()
                    print("Create")
        
                    Clients.dump_conf()
    elif (com == '2'):
        print("Load")
        name = input("[NAME]: ")
        
        if name in Clients.data["NAME"]:
            selected_name = name # Должна быть проверка на существования Profile
            Logs.data = "[+] Choose SELECTED_NAME: {}".format(selected_name)
            Logs.dump_conf()
        else:
            print("Error!")
    elif (com == '3'):
        print("Delete")
        name = input("[NAME]: ")
    
        if (selected_name == name):
            print("Do you want to delete the selected name?\n\t(1/Other -> Yes/No)\n")
            
            if (input(" => ") != '1'):
                return True
                
            selected_name = ""
            Logs.data = "[+] Choose SELECTED_NAME: {}".format(selected_name)
            Logs.dump_conf()
            
        try:
            index = Clients.data["NAME"].index(name)
            Logs.data = "[+] Delete PROFILE: {}@{}:{}".format(name, Clients.data["IP"][index], Clients.data["PORT"][index])
            Logs.dump_conf()
                
            Clients.data["NAME"].pop(index)
            Clients.data["IP"].pop(index)
            Clients.data["PORT"].pop(index)
            Clients.data["ONLINE"].pop(index)
            Clients.dump_conf()
        except ValueError:
            print("'{}' is not in list".format(name))
    elif (com == '4'):
        print(Clients.data)
    elif (com == '5'):
        for serv in online_servers:
            print(serv.name, end = " ")
            
        print("\n")
    elif (com == '99'):
        Logs.data = "Exite menu_profile"
        Logs.dump_conf()
        print("Exit")
        
        return False
    
    return True
    
########################################

if __name__ == "__main__":
    selected_name = ""
    end = True
    online_servers = list()
    procs = list()
    Logs = main(online_servers, procs, end)
    end = False
    del(Logs)
