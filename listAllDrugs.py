import xml.etree.ElementTree as ET
import os

listOfFiles = os.listdir('./Train/MedLine/')
for i in listOfFiles:
	str = 'Train/MedLine/'+i
	tree = ET.parse(str)
	root = tree.getroot()
	for c in root:
		for e in c.iter('entity'):
			print e.attrib['text']
