import requests
import csv
from xml.dom.minidom import parseString

# IrishRail Api url:
url = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML'

page = requests.get(url)

doc = parseString(page.content)

# print the content of the page to check if the code worked so far
#print(doc.toprettyxml())

with open("trainxml.xml", "w") as xmlfp:
    doc.writexml(xmlfp)

  
objTrainPositionsNodes = doc.getElementsByTagName("objTrainPositions")

for objTrainPositionsNode in objTrainPositionsNodes:
    trainCodeNode = objTrainPositionsNode.getElementsByTagName("TrainCode").item(0)
    trainCode = trainCodeNode.firstChild.nodeValue.strip()

    trainLatNode = objTrainPositionsNode.getElementsByTagName("TrainLatitude").item(0)
    trainLat = trainLatNode.firstChild.nodeValue.strip()

    trainLongNode = objTrainPositionsNode.getElementsByTagName("TrainLongitude").item(0)
    trainLong = trainLongNode.firstChild.nodeValue.strip()    

    print("Traincode: {}, Latitude: {}, Longitude: {}".format(trainCode, trainLat, trainLong))
    