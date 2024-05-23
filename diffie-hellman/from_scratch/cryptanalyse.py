# parametres
p=23
g=5

# Ayant recupérer la clé publique du client lors de l'échange, il est possible de retrouver la clé publique si le modulo est petit.
pubC=20 # g^x mod p on test tous les x possibles

for i in range(2,23):
    val=pow(g,i,p)
    if val==pubC:
        print("private key X=", i)
        break
    
