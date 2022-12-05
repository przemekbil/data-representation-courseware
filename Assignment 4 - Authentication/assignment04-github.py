# DATA REPRESENTATION Assignment 04
# Author: Przemyslaw Bil

import requests
from config import config

# Function to fetch the list of files in the main folder of the repository
# NOTE: this function will not scan subfolders and will return files in the root folder of the repository only
# each containing file name, url and content in string format
def getFilesContent(baseUrl, apiKey):

    files=[]

    content_url = "{}/contents".format(baseUrl)
    # get the content of the repository
    response = requests.get(content_url, auth=('token', apiKey))
    content = response.json()

    # print filenames in the repository
    for repo_element in content:
        file_url = repo_element["download_url"]

        #print("\nFile name: {} \n".format(repo_element["name"]))
        #print("\nFile url: {} \n".format(file_url))

        # Ignore subfolders
        if file_url:
            # get the content of each file
            response = requests.get(file_url, auth=('token', apiKey))

            file={
                "name": repo_element["name"],
                "url": file_url,
                "content":response.text
            }

            files.append(file)

    # return the list of dictionary objects
    # each containing file name, url and content in string format
    return files


# Function to replace the names in the files
# IN list of files as dictionary objects, original name, name to change to
def swapNameInFiles(filesIn, nameIn, nameOut):

    files_out=[]

    for file in filesIn:

        file_out={
            "name": file["name"],
            "url": file["url"],
            "content": file["content"].replace(nameIn, nameOut)
        }              

        files_out.append(file_out)

    # return the list of dictionary objects
    # each containing file name, url and content in string format with name swapped   
    return files_out

def uploadchangesAndCommit(base_repo_url, apiKey, file, org_name, new_name):

    # This function cretaed as per the thread below:
    #https://stackoverflow.com/questions/11801983/how-to-create-a-commit-and-push-into-repo-with-github-api-v3

    # Get the latest commit SHA of the main branch
    response = requests.get("{}/branches/main".format(base_repo_url), auth=('token', apiKey))
    last_commit_sha = response.json()['commit']['sha']

    # Change the content of the file
    content={
    "content": file['content'],
    "encoding": "utf-8"
    }
    response = requests.post("{}/git/blobs".format(base_repo_url), json=content, auth=('token', apiKey))
    blob_sha = response.json()['sha']


    # Create a tree which defines the folder structure
    content = {
    "base_tree": last_commit_sha,
    "tree": [
        {
        "path": file['name'],
        "mode": "100644",
        "type": "blob",
        "sha": blob_sha
        }
    ]
    }
    response = requests.post("{}/git/trees".format(base_repo_url), json=content, auth=('token', apiKey))
    tree_sha = response.json()['sha']


    # Create the commit
    content = {
        "message": "Author name changed from {} to {} in file {}".format(org_name, new_name, file['name']),
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


    # Update the reference of your branch to point to the new commit SHA
    content = {
        "ref": "refs/heads/main",
        "sha": new_commit_sha
    }

    response = requests.post("{}/git/refs/heads/main".format(base_repo_url), json=content, auth=('token', apiKey))

    # return the response from the POST request
    return response


if __name__ == "__main__":

    # import GitHub api key form the config file
    apiKey = config["myKey"]

    # repository details
    owner = "przemekbil"
    repository = "private_rep"
    # Names
    original_name = "Andrew"
    new_name = "Przemek"

    base_repo_url =  "https://api.github.com/repos/{}/{}".format(owner, repository)
   

    # get all the files form the root directory of the repository
    original_files = getFilesContent(base_repo_url, apiKey)

    # Change name in all files
    ammended_files = swapNameInFiles(original_files, original_name, new_name)

    # upload the changes and commit for each file
    for file in ammended_files:
        result = uploadchangesAndCommit(base_repo_url, apiKey, file, original_name, new_name)
        print(" File {}: {}".format(file["name"], result))
