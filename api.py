from cryptocurrency.cryptocurrency import Cryptocurrency
from flask import Flask, jsonify, request
import sys, requests

try:
    PORT_ADDRESS = sys.argv[1]
except IndexError:
    print("Usage: python command_line.py PORT_NUMBER")
    sys.exit(1)

app = Flask(__name__)
blockchain = Cryptocurrency(PORT_ADDRESS)

@app.route("/mine_block", methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_block["proof"])
    block = blockchain.create_block(proof, previous_hash)
    if block:
        response = {'message': 'Block mined successfully', 'block': block}
    else:
        response = {'message': "Block can't be mined as there are no pending transactions", 'block': block}
    return jsonify(response), 200

@app.route("/add_transaction", methods = ['POST'])
def add_transaction():
    json = request.get_json()
    if json == None:
        response = {'message':"kuchh ni aaya"}
        return jsonify(response)
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return "Some elements of transaction are missing", 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'Transaction will be added to the block {index}'}
    return jsonify(response), 201

@app.route("/get_chain", methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route("/destroy_node", methods = ['GET'])
def destroy_node():
    blockchain.destroy()
    response = {'message': f'Node with PORT NO {PORT_ADDRESS} is destroyed'}
    return jsonify(response), 200

@app.route("/update_chains", methods = ['GET'])
def update_chains():
    network = blockchain.nodes
    for node in network:
        if node != blockchain.PORT_ADDRESS:
            requests.get(f'http://0.0.0.0:{node}/update_chain')
    response = {'message': 'All chains in the network are updated'}
    return jsonify(response), 200

@app.route("/update_chain", methods = ['GET'])
def update_chain():
    is_changed = blockchain.replace_chain()
    if is_changed:
        response = {'message': 'Chains is updated'}
    else:
        response = {'message': 'Chains is ok'}
    return jsonify(response), 200


@app.route("/update_nodes", methods = ['GET'])
def update_nodes():
    network = blockchain.nodes
    for node in network:
        if node != blockchain.PORT_ADDRESS:
            requests.get(f'http://0.0.0.0:{node}/update_node')
    response = {'message': 'All the nodes in the network are updated'}
    return jsonify(response), 200

@app.route("/update_node", methods = ['GET'])
def update_node():
    blockchain.update_node()
    response = {'message': f'Node with PORT No. {PORT_ADDRESS} updated.'}
    return jsonify(response), 200

@app.route("/is_valid", methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': "Chain is valid"}
    else:
        response = {'message': "Chain is not valid"}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = PORT_ADDRESS, threaded=True)
