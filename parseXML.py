import xml.etree.ElementTree as ET
import os
import nltk

def main():
	listOfFiles = os.listdir('./Train/drugBankMedLine/')
	f = open('text.txt', 'w')
	for i in listOfFiles:
		str = 'Train/drugBankMedLine/'+i
		#str = 'Zaleplon_ddi.xml'
		tree = ET.parse(str)
		root = tree.getroot()	

		for child in root:
			text = child.attrib['text']
			#print text
			#f.write(text)
			#print '-------------------'
	
			for p in child.iter('pair'):
				if p.attrib['ddi'] == 'true':
					print text
					print 'true ...', p.attrib['id'], p.attrib['e1'], p.attrib['e2'], p.attrib['type']
					for e in child.iter('entity'):
						if e.attrib['id'] == p.attrib['e1'] or e.attrib['id'] == p.attrib['e2']:
							print e.attrib['text'] 	
		'''
			p1 = p.attrib['e1']
			p2 = p.attrib['e2']
			charOffset=[]
			for e in child.iter('entity'):
				if e.attrib['id'] == p1 or e.attrib['id'] == p2:
					charOffset.append(e.attrib['charOffset'])
		'''
	'''
	f.close()
	f = open('text.txt').read()
	fdist = nltk.FreqDist(nltk.word_tokenize(f))
	for i in range(0, len(fdist)):
		if fdist.values()[i] > 10:
			print fdist.keys()[i]#, fdist.values()[i]
	'''		
if __name__ == '__main__':
	main()
