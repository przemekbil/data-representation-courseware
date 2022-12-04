import requests
import json

# Url of exchequer account (historical series) dataset from the CSO website
url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FIQ02/JSON-stat/2.0/en"

# get the data using requests
dataset = requests.get(url)

# save the dataset in the JSON format using json.dump()
# as per https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
with open("cso.json", "w") as outfile:
    json.dump(dataset.json(), outfile)
