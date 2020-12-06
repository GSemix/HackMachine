# coding: utf-8

import subprocess
#from socket import socket
#from socket import AF_INET
#from socket import SOCK_DGRAM
import socket
#from time import sleep
from hashlib import md5

def HashMD5(words):
    return md5(words.encode("utf-8")).hexdigest()

def EnCrypt(message, messageHesh):
#    print("имя: " + message)
#    print("хэш: " + messageHesh)
    messageCrypt = ""

    k = 0
    boool = True
    for x in message:
        if k < 32 and boool:
            messageCrypt += chr(ord(x) + ord(messageHesh[k])) + messageHesh[k]
            if k == 31:
                k = 0
                boool = False
            else:
                k += 1
        else:
            if k == 32:
                k = 0
            messageCrypt += chr(ord(x) + ord(messageHesh[k]))
            k += 1
#        print(x + " => " + messageCrypt)

    if k < 32 and boool:
        messageCrypt += messageHesh[k:]

    print(messageCrypt)
    return messageCrypt

def start_serv ():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("192.168.0.15", 9001))
    
    return sock
    
def filter (sock, mess, addr):
    mess = mess.decode("utf-8").split()
    
    if (mess[0] == "hello"):
        sock.sendto("{} Encrypted_Key".format(EnCrypt("semix", HashMD5("semix"))).encode("utf-8"), addr)
        print("hello")



def main ():
    while True:
        mess, addr = sock.recvfrom(1024)
        print(addr)
        filter(sock, mess, addr)

if __name__ == '__main__':
    sock = start_serv()
    main()
    sock.close()
    
    
    
    
    """def main ():
    pr = subprocess.Popen("bash", stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    pr.stdin.write("pwd".encode())
    pr.stdin.close()
    pwd = pr.stdout.read().decode()
    print(pwd)

    pr = subprocess.Popen("bash", cwd=pwd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    pr.stdin.write("la -la".encode())
    pr.stdin.close()
    pwd = pr.stdout.read().decode()
    print(pwd)
###############
    #command = "ping 8.8.8.8 -c 5 > file.txt"
    #subprocess.Popen(command, shell = True)
    #subprocess.check_output('ps | grep -i "{}"'.format(command), shell = True)
    #pr1 = subprocess.Popen("ps", shell = True, stdout = subprocess.PIPE)
    #pr2 = subprocess.Popen("grep -i 'ping 8.8.8.8'", shell = True, stdout=subprocess.PIPE, stdin=pr1.stdout)
    #out = pr2.communicate()[0].decode().split()[0]
    #print(out)
    #try:
        #subprocess.run("tail -f file.txt".format(out), shell = True)
    #except KeyboardInterrupt:
        #subprocess.Popen("kill".split())
    #print("Hello!")"""
