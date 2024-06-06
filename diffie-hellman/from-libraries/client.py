from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import load_pem_public_key
import requests
import base64

server_ad = "http://127.0.0.1:5000"
# generer les parametres
parameters = dh.generate_parameters(generator=2, key_size=2048)
# generer la cle prive du  server
private_key_client = parameters.generate_private_key()
# Calcul de la clé publique du client
public_key_client= private_key_client.public_key()
print(public_key_client) # à supprimer

pemClient_public_key = public_key_client.public_bytes(encoding=serialization.Encoding.PEM, 
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)
# donnees à envoyer au server :
data = {"public_key": pemClient_public_key.decode()}
print("données à envoyer au server :" ,data) # à  supprimer
response = requests.post(f'{server_ad}/key_exchange' ,json = data)
if response.status_code == 200:
          server_data = response.json()
          # one recupere la  cle public du server au format pem
          server_public_key = server_data['public_key']
          # convertir la cle public du server au format DHPublicKey
          DHServer_public_key = serialization.load_pem_public_key(server_public_key.encode())
          # on calcul ensuite la clé partagée 
          shared_key =private_key_client.exchange(DHServer_public_key)
          print("cle partage (base64): ", base64.b64encode(shared_key.decode()))
else:
          print("Error de reception :"  , response.text)          
          

