# DATA REPRESENTATION Assignment 04

import requests
import json
from urllib.parse import urljoin
from config import config

apiKey = config["myKey"]

owner = "przemekbil"
repository = "private_rep"
#repository = "data-representation-courseware"

apiUrl =  urljoin("https://api.github.com/repos/", owner + "/" + repository + "/contents")
print(apiUrl)

# get the content of the repository
response = requests.get(apiUrl, auth=('token', apiKey))

content = response.json()

# print filenames in the repository
for repo_element in content:
    file_url = repo_element["download_url"]


    print("\nFile name: {} \n".format(repo_element["name"]))
    # get the content of each file
    response = requests.get(file_url, auth=('token', apiKey))

    print(response.text)

# write to file
with open("github.json", "w") as outfile:
    json.dump(content, outfile, indent=4)

#print(response.json())