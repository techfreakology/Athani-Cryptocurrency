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

vis = {}
result = ""

def search(node):
    global vis
    global result
    vis[node] = True
    # Parameters for next query
    params = {'s': s, 'x': node[0], 'y': node[1]}
    
    # Response for next step
    data = request(params)
    
    letter = data['letter']
    end = data['end']
    adjacent = data['adjacent']
    result += letter
    
    if(end):
        return True

    # traversing adjacent nodes
    for adj in adjacent:
        adj_node = (adj['x'],adj['y'])
        if adj_node not in vis.keys():
            if(search(adj_node)):
                return True
            result += letter
    
    return False

# Convert response in json form
data = response.json()

# Initial points
end = data['end']
x = 0
y = 0

start_node = (0,0)
search(start_node)
print(result)
print(s)