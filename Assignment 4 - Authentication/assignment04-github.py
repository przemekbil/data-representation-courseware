# DATA REPRESENTATION Assignment 04
# Author: Przemyslaw Bil

import requests
import json
from config import config

# import GitHub api key form the config file
apiKey = config["myKey"]

owner = "przemekbil"
repository = "private_rep"

base_repo_url =  "https://api.github.com/repos/{}/{}".format(owner, repository)


def getFilesContent(baseUrl):

    files=[]

    content_url = "{}/contents".format(baseUrl)
    # get the content of the repository
    response = requests.get(content_url, auth=('token', apiKey))
    content = response.json()

    # print filenames in the repository
    for repo_element in content:
        file_url = repo_element["download_url"]

        #print("\nFile name: {} \n".format(repo_element["name"]))
        # get the content of each file
        response = requests.get(file_url, auth=('token', apiKey))

        file={
            "name": repo_element["name"],
            "url": file_url,
            "content":response.text
        }

        files.append(file)

    return files


def swapNameInFiles(filesIn, nameIn, nameOut):

    files_out=[]

    for file in filesIn:
        file_out={
            "name": file["name"],
            "url": file["url"],
            "content": file["content"].replace(nameIn, nameOut)
        }              

    files_out.append(file_out)
    
    return files_out


original_files = getFilesContent(base_repo_url)

ammended_files = swapNameInFiles(original_files, "Andrew", "Przemek")

for file in ammended_files:
    print(file["content"])


commit_url = base_repo_url + "/git/commits"

commit={
    'message':'Test commit'
}

commit_response = requests.post(commit_url, commit)

print(commit_response)

# write to file
with open("github.json", "w") as outfile:
    json.dump(content, outfile, indent=4)