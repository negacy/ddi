import xml.etree.ElementTree as ET
import os

listOfFiles = os.listdir('./Train/testdataDrugMedLine/')#drugBankMedLine/')
for xmlFile in listOfFiles:
	f = open('./opendmapInput_testdata/' + xmlFile,'w')
	tree = ET.parse('./Train/testdataDrugMedLine/'+xmlFile)#drugBankMedLine/'+xmlFile)
	root = tree.getroot()
	for child in root:
		id = child.attrib['id']
		text = child.attrib['text']
		charOffset = [] 
		for e in child.iter('entity'):
			charOffset.append(e.attrib['charOffset'])
			#charOffset += ','
		#print id, '>>', text, '>>', charOffset
		f.write(id)
		f.write(' >> ')
		f.write(text.strip())
		if len(charOffset) > 0:
			f.write(' >> ')
			f.write(','.join(charOffset))
		f.write('\n')
	print 'done..............', xmlFile
	f.close()
