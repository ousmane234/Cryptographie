from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key

parameters = dh.generate_parameters(generator=2, key_size=1024)
# In a real handshake the peer is a remote client. For this
# example we'll generate another local private key though. Note that in
# a DH handshake both peers must agree on a common set of parameters.
private_key_server = parameters.generate_private_key()
# Calcul de la clé publique du client
public_key = private_key_server.public_key()


private_pem=private_key_server.private_bytes(encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.NoEncryption()
)

print("Private Key:", private_pem)

privkey = load_pem_private_key(private_pem, password=None)
print("Recupération ", isinstance(privkey, dh.DHPrivateKey))





public_pem=public_key.public_bytes(encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo)

print("Public Key:", public_pem)

pubkey = load_pem_public_key(public_pem)
print(isinstance(pubkey, dh.DHPublicKey))