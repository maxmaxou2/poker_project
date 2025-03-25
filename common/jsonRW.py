import json

def readJSON(path) :
    with open(path, "r") as json_file:
        loaded_data = json.load(json_file)
        return loaded_data
    
def writeJSON(path, data) :
    with open(path, "w") as json_file:
        json.dump(data, json_file)