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

#for file in ammended_files:
#    print(file["content"])


#https://stackoverflow.com/questions/11801983/how-to-create-a-commit-and-push-into-repo-with-github-api-v3
# GET /repos/:owner/:repo/branches/:branch_name

# Get the latest commit SHA of the main branch
response = requests.get("{}/branches/main".format(base_repo_url), auth=('token', apiKey))

last_commit_sha = response.json()['commit']['sha']

print(last_commit_sha)


# cerate a vontent of the file
content={
 "content": ammended_files[-1]['content'],
 "encoding": "utf-8"
}
# POST /repos/:owner/:repo/git/blobs
response = requests.post("{}/git/blobs".format(base_repo_url), json=content, auth=('token', apiKey))

utf8_blob_sha = response.json()['sha']

print(utf8_blob_sha)


# Create a tree which defines the folder structure
# POST repos/:owner/:repo/git/trees/
content = {
   "base_tree": last_commit_sha,
   "tree": [
     {
       "path": ammended_files[-1]['name'],
       "mode": "100644",
       "type": "blob",
       "sha": utf8_blob_sha
     }
   ]
 }
response = requests.post("{}/git/trees".format(base_repo_url), json=content, auth=('token', apiKey))


tree_sha = response.json()['sha']

print("Tree SHA: {}".format(tree_sha))


# Create the commit
# POST /repos/:owner/:repo/git/commits


content = {
    "message": "Author name corrected",
    "author": {
        "name": "Przemyslaw Bil",
        "email": "g00398317@atu.ie"
        },
    "parents": [
        last_commit_sha
        ],
    "tree": tree_sha
 }

commit_response = requests.post("{}/git/commits".format(base_repo_url), json=content, auth=('token', apiKey))

new_commit_sha = commit_response.json()['sha']

print("New commit SHA: {}".format(new_commit_sha))



# Update the reference of your branch to point to the new commit SHA
# POST /repos/:owner/:repo/git/refs/heads/master
content = {
     "ref": "refs/heads/main",
     "sha": new_commit_sha
 }

response = requests.post("{}/git/refs/heads/main".format(base_repo_url), json=content, auth=('token', apiKey))


print("Final update: {}".format(response))

#commit_url = base_repo_url + "/git/commits"

#commit={
#    'message':'Test commit'
#}

#commit_response = requests.post(commit_url, commit)

#print(commit_response)

# write to file
#with open("github.json", "w") as outfile:
#    json.dump(content, outfile, indent=4)