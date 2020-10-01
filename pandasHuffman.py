import heapq
import pandas as pd

class huff:

	def __init__(self,WordList=[],inputF=0):
		self.inputF=inputF
		##if series is 1 it translates WordList from pandas to list, and returns pandas the encoded result
		if self.inputF == 1:
			self.WL=WordList.tolist()
		else :
			self.WL = WordList

		self.frekans=self.calculateFreq(self.WL)

		self.key=self.createTree(self.frekans) #list form

	
		self.keyDict=self.keytoDict(self.key)
		
	
			

	def calculateFreq(self,WordList):
		frekans={}
		for i in WordList:
			for k in i:
				if k in frekans:
					frekans[k]+=1
				else:
					frekans[k]=1
		return frekans

	def encode(self,WordList,keyDict):

		encoded=[]
		for i in WordList:
			stri=""
			for j in i:
				stri+=keyDict[j]
			encoded.append(stri)

		if self.inputF == 0:
			return encoded
		if self.inputF == 1:
			return pd.Series(encoded)

	def createTree(self,frekans):

	    heap = [[weight, [symbol, '']] for symbol, weight in frekans.items()]
	    heapq.heapify(heap)

	    while len(heap) > 1:
	        low = heapq.heappop(heap)
	        high = heapq.heappop(heap)
	        for i in low[1:]:
	            i[1] = '0' + i[1]
	        for i in high[1:]:
	            i[1] = '1' + i[1]
	        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])

	    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


	def keytoDict(self,key):
		keyDict={}
		for i in key:
			keyDict[i[0]]=i[1]
		return keyDict


	def decode(self,encoded=[],key={}): 	
		decoded=[]
		for kelime in encoded:
			temp="";text=""
			for k in kelime:
				temp+=k
				for y in key:
					if temp == key[y]:
						text+=y
						temp=""

			decoded.append(text)
			
		return decoded
	




liste=["berkay","ozdemir","science","data","machine","learning"]


pdList=pd.Series(liste)
print(type(pdList))

x=huff(pdList,inputF=1)
frekans=x.calculateFreq(x.WL)
key=x.createTree(frekans)
print(key)
print(x.keyDict)
print(x.keytoDict(key))

print( "encoded:::", x.encode(x.WL,x.keyDict) )
print( "decoded::" , x.decode( x.encode(x.WL,x.keyDict) , x.keyDict ) )

#listeEncoded=x.encode()






