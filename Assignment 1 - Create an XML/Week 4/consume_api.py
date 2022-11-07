import urllib.parse
import requests


url = "http://andrewbeatty1.pythonanywhere.com/books"

def getAllBooks():

    response = requests.get(url)
    return response.json()

def getBookById(id):
    geturl = url + "/" + str(id)
    response = requests.get(geturl)

    return response.json()

def createBook(book):

    response = requests.post(url, json=book)
    return response.json()

def updateBook(id, bookdiff):
    idurl = url + "/" + str(id)
    response = requests.put(idurl, json=bookdiff)

    return response.json()


def deleteBook(id):
    idurl = url + "/" + str(id)
    response = requests.delete(idurl)

    return response.json()



if __name__=="__main__":

    book={
        'Author': 'Fiddleford Hadron McGucket', 
        'Price': 500, 
        'Title': 'Computermajigs', 
        }

    bookdiff={
        'Price': 100, 
        }
    
    print(updateBook(220, bookdiff))