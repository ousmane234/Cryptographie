import flask
import random

app = flask.Flask(__name__)

# Paramètres de domaine prédéfinis
prime = 23
generator = 5

client_shared_keys={}

# Clé privée du serveur (générée aléatoirement)
private_key_server = random.randint(1, prime - 1)

# Calcul de la clé publique du client
public_key = pow(generator, private_key_server, prime)

# Fonction pour calculer la clé partagée
def calculate_shared_key(client_public_key):
    shared_key = pow(client_public_key, private_key_server, prime)
    return shared_key

@app.route('/key_exchange', methods=['POST'])
def key_exchange():
    data = flask.request.json
    
    if 'public_key' in data:
        client_public_key = data['public_key']
        # Calculer la clé partagée avec la clé publique du client
        shared_key = calculate_shared_key(client_public_key)
        # Enregistrer la clé partagée avec le client (ne pas inclure dans la réponse)
        client_shared_keys[flask.request.remote_addr] = shared_key
        # Envoyer uniquement la clé publique du serveur au client

        # Imprimer les informations reçues
        print("Client Public Key:", client_public_key)
        print("Shared Key (Client):", shared_key)
        return flask.jsonify({'public_key': public_key})
    
    else:
        return flask.jsonify({'error': 'Client public key not found'})

if __name__ == '__main__':
    app.run(debug=True)
