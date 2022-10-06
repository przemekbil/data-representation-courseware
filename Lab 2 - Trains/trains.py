import requests
import csv
from xml.dom.minidom import parseString

# IrishRail Api url:
url = 'http://api.irishrail.ie/realtime/realtime.asmx/getCurrentTrainsXML'

retrieveTags=['TrainStatus',
'TrainLatitude',
'TrainLongitude',
'TrainCode',
'TrainDate',
'PublicMessage',
'Direction'
]
page = requests.get(url)

doc = parseString(page.content)

# print the content of the page to check if the code worked so far
#print(doc.toprettyxml())

with open("trainxml.xml", "w") as xmlfp:
    doc.writexml(xmlfp)

with open('train.csv', mode ='w', newline='') as train_file:
    train_writer = csv.writer(train_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  
    objTrainPositionsNodes = doc.getElementsByTagName("objTrainPositions")

    for objTrainPositionsNode in objTrainPositionsNodes:

        dataList = []

        # Show only Trains goinf to or from Cork
        if "Cork" in objTrainPositionsNode.getElementsByTagName("PublicMessage").item(0).firstChild.nodeValue.strip():

            for retrieveTag in retrieveTags:
                datanode = objTrainPositionsNode.getElementsByTagName(retrieveTag).item(0)            
                dataList.append(datanode.firstChild.nodeValue.strip())

            train_writer.writerow(dataList)