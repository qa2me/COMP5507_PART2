from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#this file conatains a function in which if you call it it will create a private key with its corrosponding public key
def generate_keys():

    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048) # publick key expo = 2^16 -1 , and key_size = 2^11

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())

    public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    #print("Private Key:")
    #print(private_pem.decode())
    #print("Public Key:")
    #print(public_pem.decode())
    #عشان نتأكد من الkeys بس خوز الكومنتس
    return private_key, public_key


if __name__ == "__main__":
    #usage
    prv,pub =generate_keys()
