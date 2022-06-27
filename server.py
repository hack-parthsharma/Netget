#!/usr/bin/python3
# License : GPL v3.0
# Created by Saman Ebrahimnezhad .
#
# This script will listen on 7575/TCP
# You can use this script personally but pay attention to the license file.

import RSA_Module
import socket
import signal
import sys

class NetgetServer:
	"""This is the main class of the server program."""

	def __init__(self):
		""" INIT """

		if len(sys.argv) > 1 and str(sys.argv[1]) != __file__: # this condition checks the script's arguments.

			try:

				self.sock = socket.socket()
				self.theFile = open(str(sys.argv[1]), 'rb') # this line opens the file that you told the script (binary).

			except:
				print("[\033[0;31m-\033[0m] Error in loading the file...")
				sys.exit(1)

			self.sock.bind(('', 7575)) # listens on 0.0.0.0:7575 .

			self.sock.listen(1)

			print("[\033[0;32m+\033[0m] Server is running...")

			signal.signal(signal.SIGINT, self.ctrlC) # if user sends SIGINT (same as ^C) signal ctrlC method will be called.

			self.listen()

		else:
			print("Usage: server.py FILENAME")

	def listen(self):
		"""This method will waiting for client."""

		try:
			self.rsa = RSA_Module.RSAClass("server")
		except:
			print("[\033[0;31m-\033[0m] Error : init RSA...")
			self.theFile.close()
			self.sock.close()
			sys.exit(1)

		while True:

			sc, address = self.sock.accept()

			self.theFile.seek(0) # the cursor will reset

			print("[\033[0;32m+\033[0m] New client : " + str(address[0]))

			ans = input("Do you want to send the file? [Y,n]> ")

			if str(ans).lower() != 'n':

				# send the file

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

				print("[\033[0;32m+\033[0m] Sending the file...")

				try:
					clientKey = sc.recv(2048) # gets the client public key
				except:
					print("[\033[0;31m-\033[0m] Error in getting the public key...")
					self.sock.close()
					self.theFile.close()
					sys.exit(1)

				try:
					p = self.theFile.read(4096)

					while p:

						sc.send(self.rsa.encrypt(p, clientKey)) # encrypt data with the client public key
						p = self.theFile.read(4096)
				except:
					print("[\033[0;31m-\033[0m] Error in uploading the data...")
					self.sock.close()
					self.theFile.close()
					sys.exit(1)

				print("[\033[0;32m+\033[0m] Done!")

			sc.close() # closes the client

	def ctrlC(self, sig, frame):
		"""This method can shut the server down."""

		ans = input("Do you want to shutdown the server? [y,N]> ")

		if str(ans).lower() == 'y':

			# shut the server down

			print("\n[\033[0;31m-\033[0m] Server is going down...")

			self.theFile.close()

			self.sock.close()

			sys.exit(0)

		else:
			# keep going
			print("[\033[0;32m+\033[0m] Server is up...")

if __name__ == '__main__':
	netget_server = NetgetServer()
