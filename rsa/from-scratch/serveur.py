# génerer une paire de clefs RSA pub=(e=7,n) et prive=(d,n)
# s'il reçoit la demande du client il lui envoie  pub=(e,n)
# s'il recoit le chiffré de la clé générée par le client, alors il calcul la clé partagé
# et l'affiche sur la console.
import flask 
import random 
app = flask.Flask("__name__")
# generation de la paire de clé publique et privé
e , p ,q = 7, 11 ,13 
n  , phi_n = p*q  , (p-1)*(q-1)
pub_key_server = { 'e':e , 'n': n}
d = pow( e , -1 , phi_n)
private_key = {"d": d, "n": n}
# Route pour  recevoir la clé  du client
@app.route('/secret_exchange' , methods =['POST'])
def secret_exchange():
	# recuperer les données envoyées par le client : 
	data = flask.request.json
	if 'secret_key_ciphered' in data :
		cipher_secret= data['secret_key_ciphered']
		# calcul de la cle partagé par le client
		secret = pow(cipher_secret , d , n)
		print(f'secret : {secret}')
		return flask.jsonify({'secret_key': secret})

	else:
		return flask.jsonify({'Error': 'client cipher secret not found'})     

# Route pour envoyer la cle pub
@app.route("/pub_key_exchange" , methods =['GET'])
def pub_key_exchange():
	return flask.jsonify({'public_key':{'e':e , 'n':n}})


if __name__ == "__main__":
	app.run(host ='localhost' , port = 5001 ,debug = True)