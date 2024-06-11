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
parameters = dh.generate_parameters(generator=2, key_size=1024)
@app.route("/parameters_exchange" ,methods =["GET"])
def parameters_exchange():
     # convertir les parametres en format pem
     pemParameters = parameters.parameter_bytes(
         encoding = serialization.Encoding.PEM ,
         format = serialization.ParameterFormat.PKCS3
     ).decode("utf-8")
     return flask.jsonify({"parameters": pemParameters})
    
private_key_server = parameters.generate_private_key()
# # Calcul de la clé publique du server
public_key = private_key_server.public_key()
@app.route('/key_exchange', methods=['POST'])
def key_exchange():
    data = flask.request.json
    #  les paramètres de connexion entre le  cliennt et le server
    if 'public_key' in data:
        pemClient_public_key = data['public_key']
        print("cle publique du client : " ,pemClient_public_key) # à supprimer
        # pemClient_public_key = client_public_key.encode()
        #0. Pour calculer la clef partagee, vous devez convertir la clef reçu du format PEM en objet DHPublicKey
        client_public_key = serialization.load_pem_public_key(pemClient_public_key.encode("utf-8"))
        print(" taille de la cle public du  client :" ,len(pemClient_public_key))
        # Calculer la clé partagée avec la clé publique du client  au format DHPublicKey 
        shared_key = private_key_server.exchange(client_public_key)
        print("cle partagé " ,shared_key)
        # Enregistrer la clé partagée avec le client (ne pas inclure dans la réponse) 
        
        client_shared_keys[flask.request.remote_addr] = shared_key

        # 1. Imprimer les informations reçues au format PEM
        print("client public key (pem): " , pemClient_public_key)
        # 2. Imprimer la clef partagee au format HEXADECIMAL et Base64
        print("shared key (hexadecimal):" + shared_key.hex())
        print("\n")
        print("shared key (base64): "+ base64.b64encode(shared_key).decode("utf-8") )
        # 3. Convertir la Clef publique au format PEM https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#pem
        pemServer_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
             format=serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")

        # Et Envoyer uniquement la clé publique du serveur au client
        return flask.jsonify({'public_key': pemServer_public_key})
    
    else:
        return flask.jsonify({'error': 'Client public key not found'})

if __name__ == '__main__':
    app.run(debug=True)
