from cryptography.hazmat.primitives.asymmetric import dh

import flask
import random

app = flask.Flask(__name__)


client_shared_keys={}

# cryptography permet d'effectuer des opéation cryptographyque dans un context réel 

# Ici nous allons l'utiliser pour faire un Key exchange DH 

# g=2 et key_size=2048 lire la document pour connaire la valeur du modulo p en fonction de la taille.
# Il est préférable et fortement conseiller d'utiliser des spécifications données par NIST (ou d'autre orga reconnues)
parameters = dh.generate_parameters(generator=2, key_size=2048)

private_key_server = parameters.generate_private_key()
# Calcul de la clé publique du client
public_key = private_key_server.public_key()



# Fonction pour calculer la clé partagée
def calculate_shared_key(client_public_key):
    shared_key = private_key_server.exchange(client_public_key)
    return shared_key

@app.route('/key_exchange', methods=['POST'])
def key_exchange():
    data = flask.request.json
    
    if 'public_key' in data:
        client_public_key = data['public_key']
        #0. Pour calculer la clef partagee, vous devez convertir la clef reçu du format PEM en objet DHPublicKey
        
        
        # Calculer la clé partagée avec la clé publique du client avec clef eu format DHPublicKey 
        shared_key = calculate_shared_key(client_public_key)

        # Enregistrer la clé partagée avec le client (ne pas inclure dans la réponse)
        client_shared_keys[flask.request.remote_addr] = shared_key

        

        # 1. Imprimer les informations reçues au format PEM
        # 2. Imprimer la clef partagee au format HEXADECIMAL et Base64
        # 3. Convertir la Clef publique au format PEM https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#pem
        # Et Envoyer uniquement la clé publique du serveur au client
        return flask.jsonify({'public_key': "à envoyer au format PEM"})
    
    else:
        return flask.jsonify({'error': 'Client public key not found'})

if __name__ == '__main__':
    app.run(debug=True)
