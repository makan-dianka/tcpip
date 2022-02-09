def password(self, len_password):
    # generateur du mdp prend 1 arg int et return la taille de l'arg, par alphanumerique + symbole
    pwd = "" 
    mot_cles = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        '&', '%', '!', '?', ':', '*', '#'
    ]
    
    for i in range(len_password):
        len_pwd5 = random.choice(mot_cles)
        pwd += len_pwd5
        
    return pwd