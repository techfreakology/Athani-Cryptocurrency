import sys
sys.path.insert(0, "../")
from blockchain.blockchain import Blockchain
from merkle.merkle import MerkleTree
import datetime
import hashlib
import json
import requests
import os

class Cryptocurrency(Blockchain):
    def __init__(self, PORT_ADDRESS):
        self.nodes = list()
        self.PORT_ADDRESS = PORT_ADDRESS
        self.transactions = []
        Blockchain.__init__(self)
        try:
            json_file_read = open('nodes.txt','r')
            data = json.load(json_file_read)
            for p in data['nodes']:
                self.nodes.append(p)
            json_file_read.close()
        except FileNotFoundError:
            print("Creating file nodes.txt...")
        finally:
            self.nodes.append(PORT_ADDRESS)
            json_file_write = open('nodes.txt','w')
            data = {"nodes": self.nodes}
            json.dump(data, json_file_write)
            json_file_write.close()
        
    def destroy(self):
        self.nodes.remove(self.PORT_ADDRESS)
        if len(self.nodes) == 0:
            os.remove("nodes.txt")
        else:
            json_file_write = open('nodes.txt','w')
            data = {"nodes": self.nodes}
            json.dump(data, json_file_write)
            json_file_write.close()

    def update_node(self):
        try:
            json_file_read = open('nodes.txt','r')
            data = json.load(json_file_read)
            self.nodes = []
            for p in data['nodes']:
                self.nodes.append(p)
            json_file_read.close()
        except FileNotFoundError:
            print("File not exist")

    def create_block(self, proof, previous_hash):
        if((len(self.transactions) == 0) and len(self.chain)>0):
            return None
        block = {'index': len(self.chain)+1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash,
                'transactions': self.transactions,
                'merkel_root': MerkleTree(self.transactions).get_root()}
        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index']+1


    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://0.0.0.0:{node}/get_chain')
            chain = response.json()['chain']
            length = response.json()['length']
            if length > max_length and self.is_chain_valid(chain):
                max_length = length
                longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def print_chain(self):
        for block in self.chain:
            print('index:',block["index"])
            print('timestamp:',block["timestamp"])
            print('proof_of_work:',block["proof"])
            print(len(block["transactions"]),"transactions:")
            for transaction in block["transactions"]:
                print("Sender: ",transaction["sender"],end=", ")
                print("Receiver: ",transaction["receiver"],end=", ")
                print("Amount: ",transaction["amount"])
            print()