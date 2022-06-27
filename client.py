#!/usr/bin/python3
# License : GPL v3.0
# Created by Saman Ebrahimnezhad .
#
# This script will connect to the server and will save the downloaded file.
# You can use this script personally but pay attention to the license file.

import RSA_Module
import socket
import signal
import sys
import os

class NetgetClient:
	"""This is the main class of the client program."""

	def __init__(self):
		""" INIT """

		if len(sys.argv) > 2 and str(sys.argv[1]) != __file__: # this condition checks the script's arguments.

			try:

				self.sock = socket.socket()
				self.sock.connect((str(sys.argv[1]), 7575))

			except:
				print("[\033[0;31m-\033[0m] Error in connecting to the server...")
				sys.exit(1)

			signal.signal(signal.SIGINT, self.ctrlC) # if user sends SIGINT (same as ^C) signal ctrlC method will be called.

			self.download()

		else:
			print("Usage: client.py SERVER_IP_ADDRESS FILENAME")

	def download(self):
		"""This method will download and save the file."""

		print("[\033[0;32m+\033[0m] Downloading the file...")

		try:

			self.theFile = open("./" + str(sys.argv[2]), 'wb') # this line opens the file that you told the script (binary).

		except:

			print("[\033[0;31m-\033[0m] Error in writing the file...")
			self.sock.close()
			sys.exit(1)

		# RSA

		# All packets are encrypted by RSA cryptography
		# The client sends the public key
		# Then the server encrypts packets with the client's public key
		# The client can decrypt packets with the private key.
		#
		# -=-=-=-=-=-=-=- SCHEMA -=-=-=-=-=-=-=-
		#
		# (SERVER)   <====REQUEST====   (CLEINT)
		# (SERVER)   =====ACCEPT====>   (CLEINT)
		# (SERVER)   <====PUB KEY====   (CLEINT)
		# (SERVER)   ===ENCRYPTED===>   (CLEINT)
		# (SERVER)   ===ENCRYPTED===>   (CLEINT)
		# (SERVER)   ===ENCRYPTED===>   (CLEINT)
		# (SERVER)   ===ENCRYPTED===>   (CLEINT)
		# (SERVER)   ======END======>   (CLEINT)
		#

		try:

			self.rsa = RSA_Module.RSAClass() # init rsa object
			self.sock.send(self.rsa.publicKey()) # sending the public key

		except:

			print("[\033[0;31m-\033[0m] Error in sending the public key...")
			self.sock.close()
			self.theFile.close()
			sys.exit(1)

		try:
			p = self.sock.recv(4096)

			while p:
				p = self.rsa.decrypt(p, self.rsa.privateKey()) # decrypt the packet with the private key
				self.theFile.write(p)
				p = self.sock.recv(4096)

			self.theFile.close()
			self.sock.close()
		except:
			print("[\033[0;31m-\033[0m] Error in connecting to the server...")
			self.sock.close()
			self.theFile.close()
			sys.exit(1)

		print("[\033[0;32m+\033[0m] Download completed!")

		sys.exit(0)

	def ctrlC(self, sig, frame):
		"""This method can cancel the downloading."""

		ans = input("Do you want to cancel the downloading file? [y,N]> ")

		if str(ans).lower() == 'y':

			# Cancel the downloading

			os.remove("./" + str(sys.argv[2]))
			self.sock.close()
			self.theFile.close()
			sys.exit(1)

if __name__ == '__main__':
	netget_client = NetgetClient()
