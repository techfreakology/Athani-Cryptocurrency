from cryptocurrency.cryptocurrency import Cryptocurrency
import sys
from subprocess import call
import os
import threading
import requests
import json

try:
	PORT_ADDRESS = sys.argv[1]
except IndexError:
	print("Usage: python command_line.py PORT_ADDRESS")
	sys.exit(1)

URL = f"http://0.0.0.0:{PORT_ADDRESS}"

def clrscr():
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f"PORT_ADDRESS: {PORT_ADDRESS}")

def callApi(PORT_ADDRESS):
    call(["python","api.py",str(PORT_ADDRESS)])

def print_json(data):
	print(json.dumps(data, sort_keys=True, indent=4))
	
# Testing the Blockchain
exit = False
while not exit:
	clrscr()
	create_blockchain = input("Do you want to create a new blockchain(Y/N): ")
	if(create_blockchain.lower() == 'y'):
		# Running api on daemon thread
		thread = threading.Thread(target=callApi,args=(PORT_ADDRESS,))
		thread.daemon = True
		thread.start()

		print("Blockchain Initialized.")
		input()

		# update the nodes list on the network
		requests.get(f'{URL}/update_nodes')

		while not exit:
			clrscr()
			choice = input("1. Mine block\n2. View blockchain\n3. Check chain validity\n4. Add transaction\n5. Exit\n")
			
			# Mine Block
			if(choice == "1"):
				response = requests.get(f'{URL}/mine_block')
				block = response.json()['block']
				message = response.json()['message']
				clrscr()
				print(message)
				if(block):
					print_json(block)
					response = requests.get(f'{URL}/update_chains')
				input()
			
			# View blockchain
			elif(choice == "2"):
				clrscr()
				response = requests.get(f'{URL}/get_chain')
				print_json(response.json()['chain'])
				input()
			
			# Check chain validity
			elif(choice == "3"):
				clrscr()
				response = requests.get(f'{URL}/is_valid')
				message = response.json()['message']
				print(message)
				input()
			
			# Add transactions
			elif(choice == "4"):
				clrscr()
				sender = input("Sender: ")
				receiver = input("Receiver: ")
				amount = input("Amount: ")
				data = {'sender': sender, 'receiver': receiver, 'amount': amount}
				response = requests.post(f'{URL}/add_transaction',json = data)
				message = response.json()['message']
				input(message)
			
			# Exit
			elif(input("Exit(Y/N): ").lower() == 'y'):
				exit = True
				clrscr()
				print(f"EXITIING {PORT_ADDRESS}")
				response = requests.get(f'{URL}/destroy_node')
				requests.get(f'{URL}/update_nodes')
				os.system(f"kill $(lsof -t -i:{PORT_ADDRESS})")
				message = response.json()['message']
				break
	
	elif(input("Exit(Y/N): ").lower() == 'y'):
		exit = True
		break