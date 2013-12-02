import xml.etree.ElementTree as ET
import os
import nltk

'''
enumerate penntreebank tags
'''
PennTreebankTags = ('CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS',\
	 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG',\
	 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WRP$', 'WRB', '.', ':', ',')

'''
DISTANCE feature - distance in words between two drugs
INPUT: sentence containing paired drugs and charoffset of corresponding drugs.
OUTPUT: distance in words
'''
def distance2Drugs(text, d1, d2):
	d1 = int(d1.split(';')[0].split('-')[1]) #last character of first drug
	d2 = int(d2.split(';')[0].split('-')[0])#first character of second drug
	return [len(text[d1+1:d2].split()), presenceOfOtherConcepts(text[d1+1:d2]),\
		presenceOfPreposition(text[d1+1:d2]), presenceOfInteractionWord(text[:d1]),\
		 presenceOfInteractionWord(text[d2:]), presenceOfInteractionWord(text[d1+1:d2])]

def distanceBigrams(text, d1, d2):
	d1 = int(d1.split(';')[0].split('-')[1])
	d2 = int(d2.split(';')[0].split('-')[0])
	tmp = [len(bigrams(text[:d1])), len(bigrams(text[d1+1:d2])), len(bigrams(text[d2:]))]
	return tmp	
def bigrams(text):
	tokens = text.split()
	return nltk.bigrams(tokens)
'''

'''	
def ddiType(text, d1, d2):
        d1 = int(d1.split(';')[0].split('-')[1])
        d2 = int(d2.split(';')[0].split('-')[0])
        tmp = presenceOfDDIType(text[:d1]) + presenceOfDDIType(text[d2:]) + presenceOfDDIType(text[d1+1:d2])
	
	return tmp

'''
returns list of 0s or 1s for each word in interactionType.txt whether they exist in the text or not.
'''
def presenceOfDDIType(text):
        ddiType = set(line.strip() for line in open('neg.txt'))#interactionTypes.txt'))
        val = []
        text = nltk.word_tokenize(text)
        for i in ddiType:
                if i in text:
                        val.append(1)
                else:
                        val.append(0)
        return val


'''
detects if there is a drug between paird drugs
return TRUE if the argument is correct otherwise it returns false

'''
def presenceOfOtherConcepts(text):
	drugs = set(line.strip() for line in open('listOfDrugs.txt'))
	val = 0
	text = nltk.word_tokenize(text)
	for i in text:
		if i in drugs:
			val += 1
	return val
'''
return true if there is preposition in the text; otherwise it returns false.
'''
def presenceOfPreposition(text):
	prepositions = set(line.strip() for line in open('prepositions.txt'))
	val = 0
	text = nltk.word_tokenize(text)
	for i in text:
		if i in prepositions:
			val = 1
	return val	

def presenceOfInteractionWord(text):
	interactionWords = set(line.strip() for line in open('interactionWords.txt'))
	val = 0
	text = nltk.word_tokenize(text)
	for i in text:
		if i in interactionWords:
			val +=1
	return val
'''
syntactic information from genia dependency parser
'''
def dependencyFromgdep(textId, text, charOffsetd1, charOffsetd2):
	str_dir = './ddiTagged_testdata/'+textId
	parsedText = open(str_dir).readlines()
	interactionWords = set(line.strip() for line in open('interactionWords.txt'))
	val = []
	c0 = int(charOffsetd1.split(';')[0].split('-')[0])	
	id = len(nltk.word_tokenize(text[:c0]))
        #id = len(nltk.word_tokenize(text[:c0])) 
        pathDrug1 = [id+1]
        while id > -1: 
                id = int(parsedText[id].split()[6])-1
                if id in pathDrug1:
                        break
                if id != -1: 
                        pathDrug1.append(id)
                else:
                        pathDrug1.append(id+1)
        c1 = int(charOffsetd2.split(';')[0].split('-')[0])
        id = len(nltk.word_tokenize(text[:c1]))
        pathDrug2 = [id+1]
       
        while id > -1: 
                id = int(parsedText[id].split()[6])-1
                if id in pathDrug2:
                        break
                if id != -1: 
                        pathDrug2.append(id)
                else:
                        pathDrug2.append(id+1)
 
		
	'''
	append distnace in dependency tree freature into the val variable.
	'''
	val.append(distanceInDependencyTree(pathDrug1, pathDrug2))	
	'''
	if any of the ancestors of a drug in the dependency tree is in the interaction words list then  set the feature value for that node
	 to 1 otherwise, it's 0.
	'''
	#print 'gdep: ', textId
        for i in pathDrug1:
                if i != 0:
                        if parsedText[i-1].split()[1] in interactionWords:
                                val.append(1)
                        else:
                                val.append(0)
                else:
                        if parsedText[i].split()[1] in interactionWords:
                                val.append(1)
                        else:
                                val.append(0)
        for j in pathDrug2:
                if j != 0:
                        if parsedText[j-1].split()[1] in interactionWords:
                                val.append(1)
                        else:
                                val.append(0)
                else:
                        if parsedText[j].split()[1] in interactionWords:
                                val.append(1)
                        else:
                                val.append(0)
        return val




'''
computes how far the drugs are on a dependency tree.
Dependency tree is generated using genia dependency parser
INPUT: a list of nodes from the root till the leafe(drug) for each drug pair
OUTPUT: distance in int.
'''	
def distanceInDependencyTree(pathDrug1, pathDrug2):
	counter = 0
	for i in pathDrug1:
		if i not in pathDrug2:
			counter +=1
	for j in pathDrug2:
		if j not in pathDrug1:
			counter +=1
	return counter
	
'''
tagInfoFromGeniatagger extracts syntactic information for 3 words before and after a drug from genia tagger
geniatagger's output is saved in ddiTagged/textId
INPUT:textId of the sentence. textId can be obtained from the xml file. Each sentence has unique Id. Each sentence is parsed using geniatagger
and output is saved as sentence id. charOffsetd1 and charOffsetd2 is charoffset for the two drugs e.g. '101-105'
OUTPUT: pos tag, chunk, and NER for each word in a list format.
'''
def tagInfoFromGeniatagger(textId, text, charOffsetd1, charOffsetd2):
	d1ForwardGeniaFeatures = []
	d1BackwardGeniaFeatures = []
	d2ForwardGeniaFeatures = []
	d2BackwardGeniaFeatures = []
	d1Forward =0 
	d1Backward =0
	d2Forward =0 
	d2Backward =0
	str_dir = './ddiTagged_testdata/'+textId
	taggedFile = open(str_dir).readlines()
	c0 = int(charOffsetd1.split(';')[0].split('-')[0]) 
	c1 = int(charOffsetd1.split(';')[0].split('-')[1]) 
	d1FrontTagsId = nltk.word_tokenize(text[:c0])
	d1BackTagsId = nltk.word_tokenize(text[c1+1:])
	counter = 0
	for l in taggedFile:
		if counter < len(d1FrontTagsId) and l.strip(): #and counter >= abs(len(d1FrontTagsId) - 3):
			try:
				d1ForwardGeniaFeatures.append(PennTreebankTags.index(l.split()[4]))
			except ValueError:
				d1ForwardGeniaFeatures.append(-1)
		counter +=1
	#counter = len(d1FrontTagsId) #genia features after first drug.
	t = 0.3
	for i in  d1ForwardGeniaFeatures[len(d1ForwardGeniaFeatures)-3:]:
		d1Forward +=t*i
		t +=0.3
		
	#print 'd1Forward: ', d1ForwardGeniaFeatures[len(d1ForwardGeniaFeatures)-3:]
	counter = 0
	for l in taggedFile:
		if counter > len(d1FrontTagsId) and l.strip():# and counter <= len(d1FrontTagsId)+3:		
			try:
				d1BackwardGeniaFeatures.append(PennTreebankTags.index(l.split()[4]))
			except ValueError:
				d1BackwardGeniaFeatures.append(-1)
		counter +=1
	t = 1
	for i in  d1BackwardGeniaFeatures[:3]:
		d1Backward +=t*i
		t -=0.3
	#print 'd1Backward: ', d1BackwardGeniaFeatures[:3] #display last three tags
	
 	c0 = int(charOffsetd2.split(';')[0].split('-')[0])
 	c1 = int(charOffsetd2.split(';')[0].split('-')[1])
	d2FrontTagsId = nltk.word_tokenize(text[:c0])
	d2BackTagsId = nltk.word_tokenize(text[c1+1:])
	counter = 0
	for l in taggedFile:
		if counter < len(d2FrontTagsId) and l.strip():# and counter >= abs(len(d2FrontTagsId) - 3):
			try:
				d2ForwardGeniaFeatures.append(PennTreebankTags.index(l.split()[4]))
			except ValueError:
				d2ForwardGeniaFeatures.append(-1)
		counter +=1	
	counter = 0
	for l in taggedFile:
		if counter > len(d2FrontTagsId) and l.strip():# and counter <= len(d2FrontTagsId)+3:
			try:
				d2BackwardGeniaFeatures.append(PennTreebankTags.index(l.split()[4]))
			except ValueError:
				d2BackwardGeniaFeatures.append(-1)
		counter +=1
	t = 0.3
	for i in d2ForwardGeniaFeatures[len(d2ForwardGeniaFeatures)-3:]:
		d2Forward += t*i
		t += 0.3
	t = 1
	for i in  d2BackwardGeniaFeatures[:3]:
		d2Backward += t*i
		t -= 0.3
	#print 'd2Forward: ', d2ForwardGeniaFeatures[len(d2ForwardGeniaFeatures)-3:]
	#print 'd2Backward: ', d2BackwardGeniaFeatures[:3] #display last three tags
	
	return [d1Forward,  d1Backward, d2Forward, d2Backward]
'''
INPUT: textId and paired drug names in list.
OUTPUT: concept from opendmap.
openDMAP is run separately from a java file for each sentences. And it's output is saved as textId
'''
def conceptFromOpendmap(textId, drugPairs):
	tmp =0
	try:
		opendmapFile = open('./opendmapOutput_testdata/'+textId)
		data = opendmapFile.readlines()
		#print ','.join(drugPairs).lower()
		for i in data:
			if i.strip().lower() ==','.join(drugPairs).lower():
				tmp = 1
				break
		opendmapFile.close()
	except IOError:
		tmp =0
	return [tmp]	
		 
'''
efficient way of comparing two lists if elements are sortable 
Order of the algorithm is: O(n*log(n))
'''
def compare(s,t):
	return sorted(s) == sorted(t)
'''
This test function tests if the features extracted by the different functions in this
program are correct or not.
INPUT: X is instance of DDI pairs for their feature value and y is the label
OUTPUT: tries to uncover errors.
	
'''
def test(X,y):
	testLines = open('./test/test.dat').readlines()
	X_test=[]
	y_test=[]
	for l in testLines:
		instance = l.split()
		instance = map(int, instance)
		X_test.append(instance[:len(instance)-1])
		y_test.append(instance[len(instance)-1:])
	for i in range(0, len(X_test)):
		if compare(X[i], X_test[i]):
			print 'No error', X[i], X_test[i]
		else:
			print 'error: ', X[i], X_test[i] 
def main():
	listOfFiles = os.listdir('./Train/testdataDrugMedLine/')#drugBankMedLine/')
	f = open('dataset_test.txt', 'wr')
	for xmlFile in listOfFiles:
		print xmlFile
		tree = ET.parse('./Train/testdataDrugMedLine/' + xmlFile)#drugBankMedLine/'+ xmlFile)
		root = tree.getroot()	
		y = []
		X = [] 
		for child in root:
			text = child.attrib['text']
			textId = child.attrib['id']
			'''	
			os.environ['text'] = text
			os.environ['id'] = child.attrib['id']
			os.system('echo $text|./test.sh > ./ddiTagged/$id')
			'''
			for p in child.iter('pair'):
				p1 = p.attrib['e1']
				p2 = p.attrib['e2']
				charOffset=[]
				pairDrugs=[]
				for e in child.iter('entity'):
					if e.attrib['id'] == p1 or e.attrib['id'] == p2:
						charOffset.append(e.attrib['charOffset']) #charoffset for each pair
						pairDrugs.append(e.attrib['text']) #drugname for each drug pair
				if p.attrib['ddi'] == 'true': #:and p.attrib['type'] == 'int':
					y.append(1)
					'''
					if p.attrib['type'] == 'effect':
						y.append(1)
					elif p.attrib['type'] == 'advise':
						y.append(2)
					elif p.attrib['type'] == 'mechanism':
						y.append(3)
					elif p.attrib['type'] == 'int':
						y.append(4)
					'''
				else:
					y.append(0)
				#print 'charOffset: ', charOffset, xmlFile
				print textId, '|', p1, '|', p2, '|'
				#print len(ddiType(text, charOffset[0], charOffset[1])), ddiType(text, charOffset[0], charOffset[1])
				#print tagInfoFromGeniatagger(textId, text, charOffset[0], charOffset[1])
				#print '*'*30, pairDrugs, conceptFromOpendmap(textId, pairDrugs)
				X.append(conceptFromOpendmap(textId, pairDrugs) + \
					distance2Drugs(text, charOffset[0], charOffset[1]) + \
					 tagInfoFromGeniatagger(textId, text, charOffset[0], charOffset[1]) + \
					distanceBigrams(text, charOffset[0], charOffset[1]) + \
					ddiType(text, charOffset[0], charOffset[1]) +\
					 dependencyFromgdep(textId, text, charOffset[0], charOffset[1]))
		tmp = 0
		for i in X:
			#f.write(str(y[tmp]))
			#tmp +=1
			#f.write('\t')
			tmp1 = 7 #start point for feature is 2, 1 is reserved 
			for j in i:
				f.write(str(tmp1) +  ':' + str(j))
				f.write('\t')
				tmp1 +=1
			f.write('\n')
		
	f.close()
	#print '*'*10, 'test on going'
	#test(X,y)
if __name__ == '__main__':
	main()
