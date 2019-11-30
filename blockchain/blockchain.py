import datetime
import hashlib
import json
import os

# Creating a Blockchain Class
class Blockchain:

	def __init__(self):
		self.chain = []
		self.create_block(proof = 1, previous_hash = '0')

	def create_block(self, proof, previous_hash):
		block = {'index': len(self.chain)+1,
				 'timestamp': str(datetime.datetime.now()),
				 'proof': proof,
				 'previous_hash': previous_hash}
		self.chain.append(block)
		return block

	def get_previous_block(self):
		return self.chain[-1]

	def proof_of_work(self, previous_proof):
		new_proof = 1
		check_proof = False
		while not check_proof:
			hash_operation = hashlib.sha256(str(new_proof**2 - 
				previous_proof**2).encode()).hexdigest()
			if(hash_operation[:4] == '0000'):
				check_proof = True
			else:
				new_proof += 1
		return new_proof

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys = True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def is_chain_valid(self, chain):
		is_valid = True
		for index in range(1,len(chain)):
			previous_block_hash = self.hash(chain[index-1])
			previous_hash = chain[index]["previous_hash"]
			if previous_hash != previous_block_hash:
				is_valid = False
				break
			proof = chain[index]["proof"]
			previous_proof = chain[index-1]["proof"]
			hash_operation = hashlib.sha256(str(proof**2 - 
				previous_proof**2).encode()).hexdigest()
			if hash_operation[0:4] != '0000':
				is_valid = False
				break
		return is_valid

	def print_chain(self):
		for block in self.chain:
			print('index:',block["index"])
			print('timestamp:',block["timestamp"])
			print('proof_of_work:',block["proof"])
			print()

