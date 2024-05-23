import requests
import random

# Adresse du serveur Flask
server_address = 'http://127.0.0.1:5000'


# Paramètres de domaine prédéfinis
prime = 23
generator = 5

# Clé privée du client (générée aléatoirement)
client_private_key = random.randint(1, prime - 1)

# Calcul de la clé publique du client
client_public_key = pow(generator, client_private_key, prime)

# Données à envoyer au serveur
data = {'public_key': client_public_key}

# Envoyer la demande au serveur
response = requests.post(f'{server_address}/key_exchange', json=data)

# Vérifier si la demande a réussi
if response.status_code == 200:
    # Extraire les données de la réponse
    response_data = response.json()
    server_public_key = response_data['public_key']
    
    # Calcul de la clé partagée côté client
    shared_key_client = pow(server_public_key, client_private_key, prime)
    
    # Imprimer les informations reçues
    print("Server Public Key:", server_public_key)
    print("Shared Key (Client):", shared_key_client)
else:
    print("Error:", response.text)
