# ce module est cré le 17/06/2021
# author   : MAKAN DIANKA
# email    : MAKAN.DIANKA@HOTMAIL.COM
# site     : makandianka.org/apropos

"""
ici est côté server. c'est programme permet de transfert des fichiers/dossiers
dans
localhost en TCP/IP
avant d'éxecuter ce programme assurez-vous que vous êtes au même reseau avec le client autrement dit avec l'appareil -
que vous voulez partager vos dossiers / fichiers.
connectez-vous au même reseau puis executer ce fichier  server.py
"""
# pour le bon fonctionnement de ce code, il est prefferable d'utiliser Python 3.XX
# le modules exigés pour executer ce programme sont :
# socket, os, sys, random, tqdm, time

import socket
import os
import sys
import random
from tqdm import tqdm
import time

import password

if sys.version_info[0] < 3:
    print("""
          CE MODDULE REQUIERT PYTHON 3.X.X
          """
          )
    sys.exit()
 
class FileTransfert:
    '''
    L'OBJET PREND 1 ARG PATH 
    
    communication tcp/ip entre serveur et client
    l'attribue self.host recuperer l'ip de l'hôte
    l'attribue self.port est le port qui sera ouvert
    l'attribue self.server_socket est un tuple(self.host, self.port)
    l'attribue self.conn demande la connexion tcp/ip
    l'attribue self.conn.bind demarre le serveur
    l'attribue self.conn.listen(2) est le nombre d'appareil qui pourront se conncter au serveur au même temp
    l'attribue self.path est le chemin du depart
    l'attribue self.filename est un variable qui va contenir les elements du self.path #voir method client pour plus d'info
    l'attribue self.new_folder est un variable qui va contenir les elements du self.path/.. #voir method client pour plus d'info
    L'affichage l'ouverture socket {self.host}:{self.port} server en ecoute ... prêt pour recevoir des liaisons
    
    la methode server_to_client() permet de recevoir puis envoyer une reponse au client
    '''
    
    
    def __init__(self, path='/'):
        self.host = socket.gethostbyname(socket.gethostname())
        self.ports = [9000, 5520, 8888, 4512, 55512, 1992, 1993, 1999, 6655, 2031]
        self.port = random.choice(self.ports)
        self.server_socket = self.host, self.port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind(self.server_socket)
        self.conn.listen(2)
        self.path = r"{}".format(path)
        self.filename = ""
        self.new_folder = ""
        print(f"\nsocket ouvert: {self.host}:{self.port}\nserver en ecoute...")
        
        
    def folder_root(self):
        # return la liste des elements dans self.path si le path existe sinon return None.
        if os.path.exists(self.path):
            listdir = os.listdir(self.path) 
            return listdir
            
            
    def server_to_client(self):
        # blog 0
        passw = password(8)
       
        # blog 1.
        # le socket et adresse du client est accept
        # ensuite afficher un msg contenant  l'adresse du client ip:port
        # puis afficher le mdp pour donner au client pour pouvoir communique
        client_socket, client_addr = self.conn.accept()
        print(f"[+] {client_addr[0]}:{client_addr[1]} est connecté")
        print(f"\n Mot de passe du serveur est : {passw}")
        
        #blog 2.
        # recevoir le mdp du client et compare au mdp du blog 1.
        mot_de_passe = client_socket.recv(1024)
        mdp = mot_de_passe.decode("utf-8")
        
        # blog 3
        # si blog 2 est egal à blog 1, le mdp est confirmé ensuite elements du self.folder_root() sera envoyé au client
        # sinon mot de passe incorrect sera envoyé et l'accée aux elements sera refusé.
        if mdp == passw:
            print(" mot de passe confirmé\n")
            
            # Blog AA. si self.folder_root() ne return pas None. il va être iteré et
            # concatener les elements dans le var self.filename
            if self.folder_root() is not None:
                for filename in self.folder_root():
                    self.filename += f"\t{filename}\n"
                
                # b 1. ENVOYER
                # envoyer le self.path et ses contenus
                # puis constituer le path self.path et ses elems encoder puis envoyer au client
                # puis afficher le self.path etant accée autorisé pour le client
                filename = f"\n{self.path}>\n\n{self.filename}".encode("utf-8")
                client_socket.sendall(filename)
                print("{} path> {} ".format("access allowed to".upper(), self.path))
                
                # b 2 RECEVOIR
                # recevoir le dossier ou fichier demandé par le client dans self.path  << self.path et ses contenus sont envoyé dans b 1.>>
                # le var path_chosen stock le path complet et prêt pour envoyer
                choise_folder = client_socket.recv(1024)
                folder_chosen = choise_folder.decode("utf-8")
                path_chosen = os.path.join(self.path, folder_chosen) 
                
                # blog AB. si le path_chosen existe sinon msg est envoyé "path specifié n'existe"
                if os.path.exists(path_chosen):
                    # ENVOYER
                    #b3 le prog verifie si folder_chosen(voir b2) est un fichier puis envoie le fichier en question
                    if "." in folder_chosen:
                        # blog AD.
                        # le fichier .ini est dans fichier. je ne peux pas envoyer sinon je l'envoie
                        if ".ini" in folder_chosen:
                            msg = f"je ne peux pas vous envoyer le fichier> {folder_chosen}"
                            encode_msg = msg.encode("utf-8")
                            client_socket.sendall(encode_msg)
                            print("{} path> {} ".format("access DANIED to".upper(), path_chosen))
                        else:
                            # blog AD
                            file_size = os.path.getsize(path_chosen)
                            file_name = path_chosen.split("\\")[2]
                            info_file = f"{file_name}@{file_size}".encode("utf-8")
                            client_socket.sendall(info_file)
                            
                            with open(path_chosen, 'rb') as b:
                                while True:
                                    byte = b.read(1024)
                                    if byte:
                                        client_socket.sendall(byte)
                                    else:
                                        break
                                
                                print("{} path> {} ".format("ACCESS ALLOWED to".upper(), path_chosen))
                                progress = tqdm(range(file_size), f"{file_name}", unit="b", unit_scale=True, unit_divisor=1024)
                                progress.update(file_size)
                                time.sleep(0.5)
                    else:
                        # b4
                        # si b3 n'est pas un fichier alors le client demande un dossier
                        # dans ce cas le prog va iterer le dossier demandé si le dossier n'est pas vide puis executé b5
                        listdir_path_chosen = os.listdir(path_chosen)
                        if len(listdir_path_chosen) > 0:
                            for elements in listdir_path_chosen:
                                self.new_folder += f"\t{elements}\n"
                            
                            # b5. ENVOYER b2 et ses contenu
                            # puis afficher un msg "accès autorisé path_chosen/new_folder".  << path_chosen/new_folder est demandé par le client dans b2>>
                            path_folder = f"\n{path_chosen}>\n\n{self.new_folder} "
                            re_send_path = path_folder.encode("utf-8")
                            client_socket.sendall(re_send_path)
                            print("{} path> {} ".format("access allowed to".upper(), path_chosen))
                        
                            # b6. RECEVOIR
                            # recevoir la demande d'un fichier dans path_chosen/self.new_folder/..  << path_chosen/self.new_folder/.. sera envoyé dans b5
                            # le var path_recv stock le path complet et prêt à envoyer
                            recv_file = client_socket.recv(1024)
                            file_name = recv_file.decode("utf-8")
                            path_recv = os.path.join(path_chosen, file_name) 
                            
                            # b 7. ENVOYER
                            # le prog verifie si b6 est un fichier puis envoie le fichier en question
                            # puis affiche accès autorisé path : path_recv dans b6
                            if "." in file_name:
                                # blog AC.
                                file_size = os.path.getsize(path_recv)
                                file_name = path_recv.split("\\")[3]
                                info_file = f"{file_name}:{file_size}"
                                client_socket.sendall(info_file.encode("utf-8"))
                                    
                                if os.path.exists(path_recv):
                                    with open(path_recv, "rb") as b:
                                        while True:
                                            byte = b.read(1024)
                                            if byte:
                                                client_socket.sendall(byte)
                                            else:
                                                break
                                        print("{} path> {} ".format("access allowed to".upper(), path_recv))
                                        progress = tqdm(range(file_size), f"{file_name}", unit="b", unit_scale=True, unit_divisor=1024)
                                        progress.update(file_size)
                                        time.sleep(0.5)
                                else:
                                    # path n'existe pas. blog AC
                                    no_exist_path = f"\nle chemin spécifié n'existe pas> {path_recv}"
                                    re_send_no_exist_path = no_exist_path.encode("utf-8")
                                    client_socket.sendall(re_send_no_exist_path)
                                    print(f"le chemin spécifié n'existe pas> {path_recv}")
                                    
                                    
                        
                        else:
                            # dossier demandé est vide
                            msg = f"\n{path_chosen}>\n\n\tvide "
                            empty_directory = msg.encode("utf-8")
                            client_socket.sendall(empty_directory)
                            print("{} path> {} ".format("access allowed to".upper(), path_chosen))
                else:
                    # path n'existe pas. blog AB
                    no_exist_path = f"\nle chemin spécifié n'existe pas> {path_chosen}"
                    re_send_no_exist_path = no_exist_path.encode("utf-8")
                    client_socket.sendall(re_send_no_exist_path)
                    print(f"le chemin spécifié n'existe pas> {path_chosen}")
                
            else:
                # path n'existe pas. bolg AA
                no_exist_path = f"\nle chemin spécifié n'existe pas> {self.path}\nce n'est pas de votre faute. Une erreur technique s'est produit de notre côté. "
                re_send_no_exist_path = no_exist_path.encode("utf-8")
                client_socket.sendall(re_send_no_exist_path)
                print(f"le chemin spécifié n'existe pas> {self.path}")
        else:
            # mot de passe incorrect
            wrong_pass = "\n mot de passe incorrect. accès refusé"
            wrong = wrong_pass.encode("utf-8")
            client_socket.sendall(wrong)
            print(' mot de passe incorrect')
            
            
obj = FileTransfert()
obj.server_to_client() 

          
# def choise_path(path):
#     if os.path.exists(f"/{path}"):
#         print(f"\nLe repertoire C:/{path} sera partagé ainsi que les fichiers et les dossiers qui contient")
#         obj = FileTransfert(path)
#         obj.server_to_client()
#     else:
#         print(f"\n Le chemin spécifié n'existe pas C:\{path}")
    
# print("\nTaper le nom d'un dossier dans la racine de votre disque C:/")  
# share_path = input("Quel dossier voulez-vous partager ? ")

# choise_path(share_path)