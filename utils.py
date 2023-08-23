import json

def read_file(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    return content

def write_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

def write_json(file_name, data):
    with open(file_name, "w") as outfile:
        json.dump(data, outfile)
        
def read_json(file_name):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
    return data
    
