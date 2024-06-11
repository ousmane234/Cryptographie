from cryptography.hazmat.primitives import  serialization , hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64 
import random
import requests
server_ad = 'http://localhost:5002' 
# demander la cle public du server 
response = requests.get(f'{server_ad}/pub_key_exchange')
if response.status_code == 200: # response ok  !
          data  = response.json()
          if("public_key" in data):
                    pemServer_public_key = data["public_key"] # cle public du server au format   pem
                    print("cle publique du server : " , pemServer_public_key)
                    # convertir   la cle public du server en format DHPubicKey
                    DHServer_public_key =  serialization.load_pem_public_key(pemServer_public_key.encode("utf-8")) 
                    #  Generation d'un nombre pseudo aleatoire 
                    secret_key = str(random.randint(1,100000)).encode("utf-8")
                    # chiffrer le secret avec  la cle public du serveur 
                    secret_key_ciphered = DHServer_public_key.encrypt(
                              secret_key,
                    	 padding.OAEP(
            			 mgf=padding.MGF1(algorithm=hashes.SHA256()),
          		 	 algorithm=hashes.SHA256(), label =None
                              ) 
		)
                    # envoyer la cle chiffré au server
                    data_secret = {"secret_key_ciphered": secret_key_ciphered.hex()}
                    response_secret = requests.post(f'{server_ad}/secret_exchange'  ,json = data_secret)
                    if response_secret.status_code ==200 :
                              print("secret key :" , secret_key.decode("utf-8"))
                    else:
                              print("Erreur d'envoie du sercret ",response_secret.json())
else:
          print("Erreur de reception de la cle publique :" ,response.json())                                         
                    
                    
