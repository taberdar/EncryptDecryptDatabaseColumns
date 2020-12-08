from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import *
import base64
import os

def makekey(plaintextpassword):
	password = plaintextpassword.encode('utf8')
	salt = bytes([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,salt=salt,iterations=100000,backend=default_backend())
	key = base64.urlsafe_b64encode(kdf.derive(password))
	key_text = key.decode('utf8')
	return key_text

def strong_encrypt(password, plaintext):
	text_key = makekey(password)
	encryption_type = Fernet(text_key.encode('utf8'))
	encrypted_text = encryption_type.encrypt(plaintext.encode('utf8')).decode('utf8')
	return encrypted_text

def strong_decrypt(password, encrypted_text):
	text_key = makekey(password)
	encryption_type = Fernet(text_key.encode('utf8'))
	try: 
		decrypted_text = encryption_type.decrypt(encrypted_text.encode('utf8')).decode('utf8')
	except Exception as e:
		print(e)
		decrypted_text = 'Numpty alert: you used the wrong password. ' + 'The password you used was ' + password + '.'
	return decrypted_text

if False:
	password = 'secret'
	plaintext = 'hello world'
	encrypted_text = strong_encrypt(password, plaintext)
	decrypted_text_no = strong_decrypt('fetid socks', encrypted_text)
	decrypted_text_yes = strong_decrypt(password, encrypted_text)
	print('password:', password)
	print('text to encrypt:', plaintext)
	print('encrypted text:', encrypted_text)
	print('decrypted text no:', decrypted_text_no)
	print('decrypted text yes:', decrypted_text_yes)
