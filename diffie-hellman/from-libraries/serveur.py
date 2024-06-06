from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
import base64
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
# Calcul de la clé publique du server
public_key = private_key_server.public_key()
@app.route('/key_exchange', methods=['POST','GET'])
def key_exchange():
    data = flask.request.json
    
    if 'public_key' in data:
        client_public_key = data['public_key']
        print("cle publique du client : " ,client_public_key) # à supprimer
        #0. Pour calculer la clef partagee, vous devez convertir la clef reçu du format PEM en objet DHPublicKey
        DHClient_public_key = serialization.load_pem_public_key(client_public_key.encode())
        # Calculer la clé partagée avec la clé publique du client  au format DHPublicKey 
        shared_key = private_key_server.exchange(DHClient_public_key)
        print("cle partagé " ,shared_key)
        # Enregistrer la clé partagée avec le client (ne pas inclure dans la réponse)
        client_shared_keys[flask.request.remote_addr] = shared_key

        # 1. Imprimer les informations reçues au format PEM
        print("client public key (pem): " , client_public_key)
        # 2. Imprimer la clef partagee au format HEXADECIMAL et Base64
        print("shared key (hexadecimal):" + shared_key.hex())
        print("shared key (base4): "+ base64.b64encode(shared_key).decode() )
        # 3. Convertir la Clef publique au format PEM https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#pem
        pemServer_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
             format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Et Envoyer uniquement la clé publique du serveur au client
        return flask.jsonify({'public_key': pemServer_public_key.decode()})
    
    else:
        return flask.jsonify({'error': 'Client public key not found'})

if __name__ == '__main__':
    app.run(debug=True)
