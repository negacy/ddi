import xml.etree.ElementTree as ET
import os
def main():
	f1 = open('/Users/negacy/Downloads/libsvm-3.16/dataset/scripts/final.txt')
	
	data = f1.readlines()
	prediction=[]
	types=[]
	for i in data:
		if i.strip().split('|')[-2] == '1':
			prediction.append('true')
		else:
			prediction.append('false')
		types.append(i.strip().split('|')[-1])
	counter=0
	listOfFiles = os.listdir('./Train/testdataDrugMedLine/')
	for xmlFile in listOfFiles:
		f2 = open('/Users/negacy/Downloads/libsvm-3.16/dataset/scripts/goldDir/'+xmlFile, 'wr')
		tree = ET.parse('./Train/testdataDrugMedLine/'+ xmlFile)
		root = tree.getroot()
		f2.write('<?xml version="1.0" encoding="UTF-8"?>')
		f2.write('\n')
		f2.write('<document id="' + root.attrib['id'].strip() +'">')
		f2.write('\n')
		for c in root:
			f2.write('<sentence id="' + c.attrib['id'].strip() + '"')
			f2.write(' text="'+c.attrib['text'].strip() +'">')
			f2.write('\n')
			for e in c.iter('entity'):
				f2.write('<entity id="' + e.attrib['id'].strip() +'"')
				f2.write(' charOffset="' + e.attrib['charOffset'].strip() +'"')
				f2.write(' type="'+ e.attrib['type'].strip() +'"')
				f2.write(' text="' + e.attrib['text'].strip()+ '"/>')
				f2.write('\n')
			for p in c.iter('pair'):
				f2.write('<pair id="' + p.attrib['id'].strip() +'"')
				f2.write(' e1="' + p.attrib['e1'].strip() + '"')
				f2.write(' e2="' + p.attrib['e2'].strip() +'"')
				f2.write(' ddi="' + prediction[counter] +'"')
				f2.write(' type="' + types[counter] +'"/>')
				f2.write('\n')
				counter +=1
			f2.write('</sentence>')
			f2.write('\n')
		f2.write('</document>')
		f2.close()
	

if __name__=='__main__':
	main()
