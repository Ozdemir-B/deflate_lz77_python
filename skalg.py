import sys
import os
import pickle
import heapq



class lz77:

	def __init__(self,txt_file="",sbSize=0,labSize=0 ):	
		
		pass


	def encode(self,text_name,sbSize,labSize):

		#searchBuffer = list()
		#LAB = list()
		text=open(text_name,"r").read()

		encoded = list() # it will be a list of triples (tuple with 3 element)
		i=0
		##----------------------- starting of the encoding process  ------------------------
		while i < len(text):
			# i used for loop before while. but i guess in python i cant increase "i" manually. only loop increases "i" one by one.
			#filling the searchBuffer and look ahead buffer with text data sequentially
			LAB=""; searchBuffer="" # dizileri sıfırlıyorum. üzerine yazılmaması için
			for a in range(labSize):
				if(a+i<len(text)):
					LAB += text[a+i]

			if(i<=sbSize):
				for b in range(i):
					searchBuffer+=text[b]

			else:
				for b in range(sbSize):
					if(b+i - sbSize < len(text)):
						searchBuffer+=text[b+i-sbSize]

	
			#print("{}-{}".format(searchBuffer,LAB)) # see the filling loop

			#case 1: first element
			if i==0 : 
				encoded.append((0,0,LAB[0]))

			#case 2:
			else :
				#case 2.1 (no match)
				if LAB[0] not in searchBuffer:   #NOTE)) if not LAB[0] in searchBuffer: is same either.
					encoded.append((0,0,LAB[0]))

				#case 2.2 (match)
				if LAB[0] in searchBuffer:
					#bint("{} - case 2.2----------".format(i))
					subLab=""
					x=0; t=0
					
					for x,y in enumerate(LAB):
						if y in searchBuffer:
							subLab+=y
							
						else:
							break
					
					#case 2.2.1 (one element match) certainly
					if x==1:
						offset=searchBuffer.find(subLab)
						offset = i - offset
						#case 2.2.1.1 (if last element)
						if(len(LAB)==1):
							encoded.append((offset,x,LAB[x-1]))
						else:
							encoded.append((offset,x,LAB[x]))

					#case 2.2.2 (several match)
					else:
						while subLab not in searchBuffer:
							x=x-1
							subLab2=subLab
							subLab=""
							for n in range(x):
								subLab+=subLab2[n]
						
						offset=searchBuffer.find(subLab)
						if i < sbSize :
							offset = i - offset
						else:
							offset = sbSize - offset
						#print("{}--{}->{}".format(searchBuffer,subLab,i))
						encoded.append((offset,x,LAB[x]))

						

					i += x

			i=i+1

		
		
		wrt=open(text_name[0:len(text_name)-4]+"_encoded_txt"+".txt","w")
		for i in encoded:
			wrt.write("-"+str(i[0])+"-"+str(i[1])+"-"+i[2]+"\n")
		wrt.close()
		
		wrt=open(text_name[0:len(text_name)-4]+"_encoded","wb"); pickle.dump(encoded,wrt) ; wrt.close()

		return encoded #list of tuple



	def decode(self,name):

		decoded="" 
		i=0
		read=open(name,"rb")
		triple=pickle.load(read)
		

		for n,i in enumerate(triple):
			if i[0]==0:
				decoded+=i[2]
			
			if(i[0]!=0):
				a=0
				o=i[0]
				while(a<i[1]):
					decoded+=decoded[len(decoded)-o]
					a+=1
				decoded+=i[2]

		wrt=open(name+"_decoded.txt","w")
		wrt.write(decoded)
		wrt.close()

		return decoded

		


class deflate:
	
	def __init__(self,file=""):
		self.frekans={}	
		self.heap=[]


	def huffman_encode(self,frekans):

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


	def encode(self,file,sb,lab):

		text_lz=lz77().encode(file,sb,lab)
		frk1={} ; frk2={} 

		for c in text_lz:
			if not c[0] in frk1:
				frk1[c[0]]=0
			frk1[c[0]]+=1

		lz_list2=list()
		for i in text_lz:
			lz_list2.append((i[1],i[2]))

		for c in lz_list2:
			if not c in frk2:
				frk2[c]=0
			frk2[c]+=1

		
		text_lz_huffed_1=self.huffman_encode(frk1)
		text_lz_huffed_2=self.huffman_encode(frk2)
		

		text1="";text2=""	
		
		for i in text_lz:
			n=0
			for n in range(len(text_lz_huffed_1)):
				if i[0] == text_lz_huffed_1[n][0]: 
					text1+=text_lz_huffed_1[n][1]

		for i in lz_list2:
			for n in range(len(text_lz_huffed_2)):
				if i == text_lz_huffed_2[n][0]:
					text2+=text_lz_huffed_2[n][1]

		key_s="";key_o=""

		for n in range(len(text_lz_huffed_2)):
				key_s+=str(text_lz_huffed_2[n][0][0])+"-"+ text_lz_huffed_2[n][0][1] +"-"+ text_lz_huffed_2[n][1] +"\n"

		for i in text_lz_huffed_1:
			key_o+=str(i[0])+"-"+i[1]+"\n"


		#writing keys for the huffman decoding
		#key_o is for the offset and key_s is for the string
		wrt_ky=open(file[0:len(file)-4]+"_key_o.txt","w");wrt_ky.write(key_o);wrt_ky.close()
		wrt_ky=open(file[0:len(file)-4]+"_key_s.txt","w");wrt_ky.write(key_s);wrt_ky.close()

		wrt_final=open(file[0:len(file)-4]+"_deflated.txt","w");wrt_final.write(text1+"\n"+text2)
					
		

	def huffman_decode(self,deflated,key_o,key_s):
		#reads from the file text and reconstructs the lz77 compressed data 
		listo=list();lists=list()
		#listo is the list of the offsets in the lz77 data with the huffman codes
		#lists is the list of strings in the lz77 data with the huffman codes

		temp_o="";temp_b="";count=0
		i=0
		
		while i < len(key_o):
			if key_o[i] is "-":
				count+=1
				i+=1
			if count is 0 :
				temp_o+=key_o[i]
			if count == 1:
				temp_b+=key_o[i]
			if key_o[i] == "\n":
				listo.append((int(temp_o),temp_b[0:len(temp_b)-1]))
				count=0
				temp_o=""
				temp_b=""
			i+=1

		i=0;temp_l=""; temp_c="";temp_b="";count=0
		while i < len(key_s):
			if key_s[i] == "-":
				count+=1
				i+=1
			if count is 0:
				temp_l+=key_s[i]
			if count is 1 :
				temp_c+=key_s[i]
			if count is 2:
				temp_b+=key_s[i]
			if key_s[i]=="\n":
				lists.append([(int(temp_l),temp_c),temp_b[0:len(temp_b)-1]])
				temp_c=""
				temp_b=""
				temp_l=""
				count=0
			i+=1

		#text_o is the huffed text for the offset of the lz77
		#text_s is the huffed text for the strings of the lz77
		text_o=""
		text_s=""
		i=0;count=0
		while i < len(deflated):
			if deflated[i] is "\n":
				count+=1
				i+=1
			if count is 0:
				text_o+=deflated[i]
			if count is 1:
				text_s+=deflated[i]
			i+=1

		text_s+="-";text_o+="-"
		lz_o=list() ; lz_s=list()
		#lz_o and _lz_s is the list of offsets and strings in lz77 list in order
		
		temp_i=""		
		for i in text_o:
			for j in listo:
				if temp_i == j[1]:
					lz_o.append(j[0])
					temp_i=""
			temp_i+=i

		
		temp_i=""
		for i in text_s:
			for j in lists:
				if temp_i == j[1]:
					lz_s.append(j[0])
					temp_i=""
			temp_i+=i

		#finally , lz is the unhuffed form of the deflate compressed data. which is lz77 compressed form.
		lz=list()
		for i in range(len(lz_s)):
			lz.append((lz_o[i],lz_s[i][0],lz_s[i][1]))
		

		#writing lz to a file to reconstruct from the lz77 form
		wrtt=open(self.file_name[0:len(self.file_name)-4]+"_unhuffed","wb");pickle.dump(lz,wrtt);wrtt.close()


	def decode(self,file,key_o,key_s): 

		deflated=open(file,"r").read()
		keyo=open(key_o,"r").read() ; keys = open(key_s,"r").read()
		self.file_name=file

		self.huffman_decode(deflated,keyo,keys)
		final_decoded=lz77().decode(file[0:len(file)-4]+"_unhuffed")	