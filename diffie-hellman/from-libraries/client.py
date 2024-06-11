from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import load_pem_public_key
import requests
import base64

server_ad = "http://127.0.0.1:5000"
#Recuperer les parametres crypto depuis le serveur qui sont au format pem
param_response = requests.get(f'{server_ad}/parameters_exchange')
param_response_data = param_response.json()

pem_parameters = param_response_data['parameters'].encode("utf-8")
parameters = serialization.load_pem_parameters(pem_parameters)
# generer la cle prive du  server à partir des clients
private_key_client = parameters.generate_private_key()
# Calcul de la clé publique du client
public_key_client= private_key_client.public_key()
print("cle publique du client :" ,public_key_client) # à supprimer
# transformer la cle publique du cliennt au format  pem
pemClient_public_key = public_key_client.public_bytes(encoding=serialization.Encoding.PEM, 
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
# donnees à envoyer au server :
data = {"public_key": pemClient_public_key}
print("données à envoyer au server :" ,data) # à  supprimer
response = requests.post(f'{server_ad}/key_exchange' ,json = data)
if response.status_code == 200:
          server_data = response.json()
          # one recupere la  cle public du server au format pem
          server_public_key = server_data['public_key']
          # convertir la cle public du server au format DHPublicKey
          DHServer_public_key = serialization.load_pem_public_key(server_public_key.encode("utf-8"))
          # on calcul ensuite la clé partagée 
          shared_key =private_key_client.exchange(DHServer_public_key)
          print("shared key (hexadecimal):" + shared_key.hex())
          print('\n')
          print("shared key (base64): "+ base64.b64encode(shared_key).decode("utf-8") )
else:
          print("Error de reception :"  , response.json)          
          

