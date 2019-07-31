import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Creating a Blockchain Class
class Blockchain:

	def __init__(self):
		self.chain = []
		self.transactions = []
		self.create_block(proof = 1, previous_hash = '0')
		self.nodes = set()

	def create_block(self, proof, previous_hash):
		block = {'index': len(self.chain)+1,
				 'timestamp': str(datetime.datetime.now()),
				 'proof': proof,
				 'previous_hash': previous_hash,
				 'transactions': self.transactions}
		self.transactions = []
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
		previous_block = chain[0]
		block_index = 1
		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False
			proof = block['proof']
			previous_proof = previous_block['proof']
			hash_operation = hashlib.sha256(str(proof**2 - 
				previous_proof**2).encode()).hexdigest()
			if(hash_operation[:4] != '0000'):
				return False
			previous_block = block
			block_index += 1
		return True

	def add_transaction(self, sender, receiver, amount):
		self.transactions.append({'sender': sender,
								  'receiver': receiver,
								  'amount': amount})
		previous_block = self.get_previous_block()
		return previous_block['index'] + 1

	def add_node(self, address):
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc)

	def replace_chain(self):
		network = self.nodes
		longest_chain = None
		max_length = len(self.chain)
		for node in network:
			response = requests.get(f'http://{node}/get_chain')
			chain = response.json()['chain']
			length = response.json()['length']
			if length > max_length and self.is_chain_valid(chain):
				longest_chain = chain
				max_length = length
		if longest_chain:
			self.chain = longest_chain
			return True
		return False

# Creating a Web App
app = Flask(__name__)

# Creating an address for node on current port
node_address = str(uuid4()).replace('-', '')

# Instantiating Blockchain
blockchain = Blockchain()

# Mining a Block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
	previous_block = blockchain.get_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)
	blockchain.add_transaction(sender = node_address, receiver = 'Piyush', amount = 1)
	block = blockchain.create_block(proof, previous_hash)
	response = {'message': 'block mined successfully!',
				'block': block}
	return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200

# Checking whether the blockchain is valid or not
@app.route('/is_valid', methods = ['GET'])
def is_valid():
	is_valid = blockchain.is_chain_valid(blockchain.chain)
	if is_valid:
		response = {'message': 'Chain is valid'}
	else:
		response = {'message': 'Something wrong with the chain'}
	return jsonify(response), 200

# Adding a new transactions to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
	json = request.get_json()
	transaction_keys = ['sender', 'receiver', 'amount']
	if not all(key in json for key in transaction_keys):
		return 'Some elements of transaction are missing', 400
	index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
	response = {'message': f'Transaction will be added to the Block {index}'}
	return jsonify(response), 201

# Decentralizing the Blockchain

# Connecting new nodes to the network
@app.route('/connect_node', methods = ['POST'])
def connect_node():
	json = request.get_json()
	nodes = json.get('nodes')
	if nodes is None:
		return 'No nodes', 400
	for node in nodes:
		blockchain.add_node(node)
	response = {'message': 'Nodes connected successfully!',
				'total_nodes': list(blockchain.nodes)}
	return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
	is_chain_replaced = blockchain.replace_chain()
	if is_chain_replaced:
		response = {'message': 'Chain was replaced as there was a longer chain on another node',
					'new_chain': blockchain.chain}
	else:
		response = {'message': 'No change',
					'chain': blockchain.chain}
	return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 5002)


