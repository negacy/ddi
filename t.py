import nltk
def gdep(textId, text, charOffsetd1, charOffsetd2):
        str = './ddiTagged/'+textId
        parsedText = open(str).readlines()
        interactionWords = set(line.strip() for line in open('interactionWords.txt'))
        val = []
        c0 = int(charOffsetd1.split(';')[0].split('-')[0])
        id = len(nltk.word_tokenize(text[:c0])) 
        pathDrug1 = [id+1]
        while id > -1:
                id = int(parsedText[id].split()[6])-1
		print parsedText[id]
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
		print parsedText[id]
                if id in pathDrug2:
                        break
		if id != -1:
                	pathDrug2.append(id)
		else:
			pathDrug2.append(id+1)
   
	print 'drug1: ', pathDrug1
	print 'durg2: ', pathDrug2 
        ''' 
        append distnace in dependency tree freature into the val variable.
        '''
        #val.append(distanceInDependencyTree(pathDrug1, pathDrug2))    
        ''' 
        if any of the ancestors of a drug in the dependency tree is in the interaction words list then  set the feature value for that node
         to 1 otherwise, it's 0.
        '''
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
k='Lopinavir/Ritonavir'
gdep('DDI-DrugBank.d485.s37', k, '0-8','10-18')

