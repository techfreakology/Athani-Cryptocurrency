import json
import requests

# Function to call api end point /step
def request(params):
    url = 'https://challenge.flipboard.com/step'
    response = requests.post(url, params = params)
    return response.json()

# Start the maze by calling /start endpoint
response = requests.get("https://challenge.flipboard.com/start")
url = response.url

# Extract s from the url
s = url[url.find('s=')+2:url.find('&')]

# Convert response in json form
data = response.json()

# Initial points
end = data['end']
x = 0
y = 0

start_node = (0,0)

vis = {}
q = []
q.append((x,y))
parent = {}
parent[(x,y)] = -1

# Breadth First Search
while not end:
    node = q.pop(0)
    print(node)

    vis[node] = True
    
    # Parameters for next query
    params = {'s': s, 'x': node[0], 'y': node[1]}
    
    # Response for next step
    data = request(params)
    
    letter = data['letter']
    end = data['end']
    adjacent = data['adjacent']
    
    
    if(end):
        end_node = node
        break

    # traversing adjacent nodes
    for adj in adjacent:
        adj_node = (adj['x'],adj['y'])
        if adj_node not in vis.keys():
            parent[adj_node] = node
            q.append(adj_node)

path = []
par = end_node
while(par != -1):
    path.append(par)
    par = parent[par]

path = path[::-1]

result = ""

for node in path:
    params = {'s': s, 'x': node[0], 'y': node[1]}
    data = request(params)
    letter = data['letter']
    result += letter
    print(node,end=" ")

print(result)