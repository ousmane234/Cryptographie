from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Fixer un nombre premier prime et generator compris entre 2 et prime-1
prime = 23
generator = 5

# Clé privée du serveur Compris entre 1 et  prime - 1
private_key_server = 6

# Dictionnaire pour stocker les clés partagées avec chaque client
client_shared_keys = {}

# Fonction pour calculer la clé partagée
def calculate_shared_key(client_public_key):
    shared_key = pow(client_public_key, private_key_server, prime)
    return shared_key

def expo (g,x,n):
    P=1
    S=g
    k=len(bin(x))-2
    if x&1==1 :
        P=P*S
    for i in range(1,k):
        S=(S*S) % n
        if (x>>i)&1!= 0:
            P=(P*S) % n
    return P

@app.route('/key_exchange', methods=['POST'])
def key_exchange():
    """Diffie-Hellman Key Exchange.
    1. Recupérer la clef du client `client_public_key` avec le paramètre JSON `public_key`
    2. Claculer la clef partagé et renger la dans `client_shared_keys`
    3. Calculer la clé publique du serveur `public_key`
    4. envoyer la clef publique du server 
    Parameters
    ----------
    public_key : number
    

    Returns
    -------
    """
    data = request.json
    if 'public_key' in data:
        client_public_key = data['public_key']
        # Calculer la clé partagé shared_key avec la clé publique du client client_public_key
        shared_key =-1
         # Enregistrer la clé partagée avec le client avec l'adresse Ip du client.
        client_shared_keys[request.remote_addr] = shared_key
        # Calculer la clé publique du serveur 
        public_key = pow(generator, private_key_server, prime)
        #Afficher la clé partagée

        # Envoyer la clé publique au client 
        return jsonify({'prime': prime, 'generator': generator, 'public_key': public_key})
    else:
        return jsonify({'error': 'Client public key not found'})

if __name__ == '__main__':
    app.run(debug=True)