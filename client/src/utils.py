import json
import os
import random
import string

def read_json(filename):
    print("Reading from file:", filename)
    with open(filename, "r") as file:
        return json.loads(file.read())

def save_json(filename, data):
    print("Saving to file:", filename)
    with open(filename, "w") as file:
        return file.write(json.dumps(data, indent=2))

def load_directory_json(directory):
    print("Loading files from:", directory)
    data = {}
    for filename in os.listdir(directory):
        tag = filename.split(".")[0]
        data[tag] = {}
        data[tag]["statuses"] = read_json(f'{directory}/{filename}')
    return data

def get_random_hex(n):
    return "".join(random.choices(string.hexdigits, k=n))
