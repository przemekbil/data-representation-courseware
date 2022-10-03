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