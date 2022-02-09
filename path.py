import os

def racine(path='/'):  
    print("\n"+path)
    for folder in os.listdir(path):
        print("\t"+folder)
     
     
        
def get_path():
    racine()
    f = ['/'] #nom du dossiers
    while True:
        #recuperer le nom du dossier et ajouter dans la liste du dossiers
        pth = input("\n-> Dossier $ ") 
        
        #si pth est dans la liste je sors dans la boucle
        if pth in ["quit", "exit", "ok", '0']:
            print("\tBye !")
            break
        
        if pth != "..":  
            f.append(pth)
            
            #constituer le path avec les dossiers dans la liste
            current = '/'.join(f)
            
            #verifier si le path existe
            if os.path.exists(current):
                
                #verifier si c'est un dossier sinon j'affiche is not directory
                if os.path.isdir(current):
                    print(current+'>') #afficher le path courrant
                    
                    #transformer le path à une liste
                    folders = os.listdir(current)

                    #si la liste n'est pas vide j'itere et j'affiche les contenu sinon j'affiche Vide
                    if len(folders) != 0:
                        for folder in folders:
                            print("\t"+folder)
                            
                    else:
                        print("\tVide")
                else:
                    print(current+'>')
                    print('\tis not directory !')
            else:
                print(current+'>')
                print('\tle chemin spécificié n\'existe pas')
                
        elif pth == "..":
            if len(f) != 1:
                #soustraire le dernier dossier dans laliste
                f.pop(len(f) - 1)
                
                # constituer le path et afficher
                previous = '/'.join(f)
                print(previous)
                
                # iterer le path et afficher les contenu
                for folder in os.listdir(previous):
                    print('\t'+folder)
            else:
                racine()
                print("\nc'est la racine ")
                  
get_path()