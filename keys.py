"""
We want to be able to log in to any generated servers from any of my dev computers.
So (and this is a ridiculous and potentially unsafe idea) we just add all of my
github public keys to the authorized_keys.
"""

import urllib.request
import json

with urllib.request.urlopen('https://api.github.com/users/classam/keys') as response:
    json_keys = response.read()
for id_key_dict in json.loads(json_keys.decode('utf-8')):
    print(id_key_dict['key'])
