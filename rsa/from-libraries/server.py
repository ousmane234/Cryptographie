from cryptography.hazmat.primitives.asymmetric import rsa , padding
from cryptography.hazmat.primitives import serialization , hashes
import flask 
app = flask.Flask("__name__")
# generationn d'une paire de cle rsa :
server_private_key = rsa.generate_private_key(
	public_exponent = 65537 ,
	key_size =1024
)
# generer une cle public à partir  de la cle prive 
server_public_key = server_private_key.public_key()
# converitir  la cle public du server au format pem
pemServer_public_key = server_public_key.public_bytes(
		encoding = serialization.Encoding.PEM , 
		format = serialization.PublicFormat.SubjectPublicKeyInfo
	).decode("utf-8")

@app.route("/pub_key_exchange", methods =["GET"])
def pub_key_exchange():
          return flask.jsonify({"public_key" : pemServer_public_key})
@app.route("/secret_exchange" , methods = ["POST"])
def secret_exchange():
          data = flask.request.json
          # recuperere le secret  chifffré par le  client au fromat hexadécimal
          secret_key_ciphered = bytes.fromhex(data["secret_key_ciphered"])
          secret_key = server_private_key.decrypt(
                    secret_key_ciphered,
                      padding.OAEP(
          		 mgf=padding.MGF1(algorithm=hashes.SHA256()),
          		  algorithm=hashes.SHA256() ,label = None
                    )
	)      
          print("cle secret: " , secret_key.decode("utf-8"))
          return flask.jsonify({"status": "success"})
          
if __name__ == '__main__':
          app.run(debug =True ,port =5002)
                  
          