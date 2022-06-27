# License : GPL v3.0
# Created by Saman Ebrahimnezhad .
#
# RSA Cipher Class
# You can use this script personally but pay attention to the license file.

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random
from base64 import b64encode, b64decode

class RSAClass:
	def __init__(self, type="client"):
		if type == "client":
			rng = Random().read

			key = RSA.generate(2048, rng)

			self.__publicKey = key.publickey().exportKey('PEM')
			self.__privateKey = key.exportKey('PEM')

	def publicKey(self):
		return self.__publicKey

	def privateKey(self):
		return self.__privateKey

	def encrypt(self, data, publicKeyObj):
		plainData = b64encode(data)

		publicKey = RSA.importKey(publicKeyObj)

		encryptionCipher = PKCS1_v1_5.new(publicKey)

		encrypted = encryptionCipher.encrypt(plainData)

		return b64encode(encrypted)

	def decrypt(self, data, privateKeyObj):
		encrypted = b64decode(data)

		privateKey = RSA.importKey(privateKeyObj)

		decryptionCipher = PKCS1_v1_5.new(privateKey)

		plainData = decryptionCipher.decrypt(encrypted, 16)

		return b64decode(plainData)
