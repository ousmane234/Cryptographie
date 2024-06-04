# demande au serveur de lui donner sa paire de clef pub=(e,n)
# Après reception, il génère une clef secrète S aléatoire < n
# chiffre la C=S^e mod n  
# envoie C au serveur et l'affiche sur la console.
import random   
import requests # type: ignore
url = "http://127.0.0.1:5001"

# demande de la paire de cle publique :
response = requests.get(f'{url}/pub_key_exchange')
if response.status_code == 200 :
	# extraire les données de la requetes :
	response_data =  response.json()
	print(response_data)
	pub_key_server =response_data["public_key"] # clé public sous forme de dictionnaire
	e = pub_key_server["e"] 
	n = pub_key_server["n"]
	# generation d'une cle secrete S aleatoire < n 
	secret_key = random.randint(1 ,n)
	# chiffrement de la cle secrete avec la cle public du server 
	secret_key_ciphered = pow(secret_key , e , n)
	data = {"secret_key_ciphered": secret_key_ciphered}
	print(data)
	# envoyer le secret au server
	response =requests.post(f'{url}/secret_exchange', json = data)
	if response.status_code ==200:
		# afficher le secret sur  la console
		print(f'cle secret : {secret_key_ciphered}')
	else:
		print("Erreur de reception du secret")	
	

else:
	print("Erreur de reception de la cle pub du server :", response.text)


