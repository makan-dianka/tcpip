# ce module est cré le 17/06/2021
# author   : MAKAN DIANKA
# email    : MAKAN.DIANKA@HOTMAIL.COM
# site     : makandianka.org/apropos

"""
ici est côté client. c'est programme permet de demander un dossier/fichier et recevoir une reponse du server
dans localhost en TCP/IP
avant d'éxecuter ce programme assurez-vous que vous êtes au même reseau avec le server et que le server est déja demarré en premier -
autrement dit demarrer d'abord le server server.py avant d'executer ce fichier client.py

"""
# pour le bon fonctionnement de ce code, il est prefferable d'utiliser Python 3.XX
# le modules exigés pour executer ce programme sont :
# socket, os, sys, tqdm, time

import socket
import os
import sys
from tqdm import tqdm
import time

if sys.version_info[0] < 3:
    print("""
          CE MODDULE REQUIERT PYTHON 3.X.X
          """
          )
    sys.exit()

class FileTransfert:
    '''
    communication tcp/ip entre client et serveur
    l'objet prend 2 args IP, PORT
    l'attribue self.socket est un tuple(ip, port)
    l'attribue self.conn demande la connexion tcp/ip
    l'attribue self.conn.connect(self.socket) demarre la connexion au socket renseigné
    si la connexion est bien passé avec le socket renseigné, un msg de succée s'affiche "connexion est etablie avec le serveur {self.ip}:{self.port}"
    
    la methode client_to_server() permet de demander et recevoir la reponse du serveur
    '''
    
    def __init__(self, IP, PORT):
        self.ip = IP
        self.port = PORT
        self.socket = self.ip, self.port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(self.socket)
        print(f"connexion est etablie avec le serveur {self.ip}:{self.port}")
        
    def client_to_server(self):
        
        # envoyer le mot de passe au server.
        # si le mot de passe est correct blog 1 sera executé sinon accès est refusé et blog 0 s'execute
        print("\nSaisissez le mot de passe du serveur pour continuer ")
        user = input("Mot de passe > ")
        mdp = user.encode("utf-8")
        self.conn.sendall(mdp)
        
        # blog 0. si mot de passe est incorrect le programme s'arrete sinon blog 1 sera en execution.
        path = self.conn.recv(1024)
        data = path.decode("utf-8")
        if "mot de passe" in data:
            print(data)
            sys.exit()
        
        else:
            # blog 1. recevoir le chemin d'accée c:/documents du server s'il existe et ses contenu s'il n'est pas vide sinon une exception va s'elever "le chemin spécifié n'existe pas"
            # Anoter : le prog verifie si il y a des fichier dans c:/documents et les ajouter tous les fichier dans une liste>> file_end=[]
            if "le chemin spécifié n'existe pas" not in data:
                spl_data = data.split("\n")
                file_end = []
                for file_name in spl_data:
                    if "." in file_name:
                        file_end.append(file_name)
        
                print(data)
        
                
                # blog 2. demander un dossier ou fichier  c:/documents/..
                # si l'element demandé est dans blog 1 --> Anoter. donc c'est un fichier qui est demandé sinon c'est un dossier
                f = input("\nchoise: write one folder or file name below to continue\n>> ")
                if f in file_end:
                    file_name = f.encode("utf-8")
                    self.conn.sendall(file_name)
                else:
                    folder = f.encode("utf-8")
                    self.conn.sendall(folder)
        
                # blog 3. recevoir le dossier ou fichier demandé c:/documents/.. <<la demande est faite dans blog 2>>
                # Anoter : si l'element reçu contient @, signifie que c'est un fichier. le prog télécharge le fichier en question et s'arrête
                pack = self.conn.recv(1024)
                pack_enc = pack.decode("utf-8")
               
                if "@" in pack_enc:
                    spl = pack_enc.split("@")
                    file_name = spl[0]
                    file_size = int(spl[1])
                    
                    with open(file_name, "wb") as b:
                        while True:
                            byte = self.conn.recv(1024)
                            if byte:
                                b.write(byte)
                            else:
                                break
                        progress = tqdm(range(file_size), file_name, unit="b",  unit_scale=True, unit_divisor=1024)
                        progress.update(file_size)
                        time.sleep(0.5)
                    sys.exit()
                
                elif "vide" in pack_enc:
                    print(pack_enc)
                    sys.exit()
                elif "le chemin spécifié n'existe pas" in pack_enc:
                    print(pack_enc)
                    sys.exit()
                elif "je ne peux pas vous envoyer le fichier" in pack_enc:
                    print(pack_enc)
                    sys.exit()
                else:
                    # blog 4. demander un fichier dans c:/documents/../.
                    print(pack_enc)
                    file_n = input("\nchoise: write one folder or file name below to continue\n>> ")
                    send_file_n = file_n.encode("utf-8")
                    self.conn.sendall(send_file_n)
                    
                    # blog 5. recevoir le fichier demandé c:/documents/../.   <<la demande est faite dans blog 4>>
                    # l'element reçu contient : signifie que c'est un fichier alors le prog télécharg le fichier en question et s'arrête
                    file_recv = self.conn.recv(1024)
                    data_decode = file_recv.decode("utf-8")
                    
                    if ':' in data_decode:
                        file_name, file_siz = data_decode.split(":")
                        file_ = int(file_siz)
                    
                        with open(file_name, "wb") as b:
                            while True:
                                byte = self.conn.recv(1024)
                                if byte:
                                    b.write(byte)
                                else:
                                    break
                            progress = tqdm(range(file_), file_name, unit="b",  unit_scale=True, unit_divisor=1024)
                            progress.update(file_)
                            time.sleep(0.5)
                
            else:
                print(data)


def server(ip, port):
    # definition objet de la class FileTransfert dans cette fonction
    # la fonction prend 2 args : ip, port
    # ensuite passer les  2 args dans l'objet de la class FileTransfert
    # puis appeler la methode client_to_server() de l'objet.
    
    obj = FileTransfert(ip, port)
    obj.client_to_server()


print("\nDonnez les informations du serveur ci-dessous")  
ip = input("\nadresse IP : ")
port = int(input("numéro de PORT : "))

server(ip, port)