# -*- coding: utf-8 -*-
import re
import os
import nltk
from nltk.corpus import stopwords
stopwordList = stopwords.words('english')
nltk_stopword_list = set(stopwords.words('english')) - set(["very","didnt","doesnt","dont","didn't","doesn't","not","never","nor",
"n't","at","all","to","have","over","in","during","but","more","most","been","being","having","do","does","did","doing","until","while",
"with","abount","against","between","through","during","below","above","down","in","under","few","each","no","nor","not",
"some","such","only","so","very",'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'])

class Rule(object):


	__instance = None

	@staticmethod
	def getInstance():
		if Rule.__instance == None:
			Rule()
		return Rule.__instance 

	def __init__(self):
		if Rule.__instance != None:
			logger.error("Rule class is a singleton!")
		else:			
			Rule.__instance = self


	def validate_opinion(self, data):
		token = [token[0].lower() for token in data]
		minus_token = nltk_stopword_list - set(token)
		if len(minus_token) > 0:
			return True
		return False

	def extract_opinion(self,data):

		result = []
		temp = []
		temp_pos = []
		prev_tag = None

		########## find verb and adjective patterns #################
		count  = 0
		for index, record in enumerate(data):
			word = record[0]
			tag = record[1]
			if tag[0:2] in ["NN"] and prev_tag != None and prev_tag[0:2] in ["VB","RB","JJ","TO","DT","IN"] and word.lower() not in nltk_stopword_list:	
				for i in range(index,len(data)):
					word , tag = data[i][0],data[i][1]
					if tag[0:2] in ["NN"]:
						temp.append((word,tag))
						temp_pos.append(tag[0:2])	
						prev_tag = tag
					else:
						result.append(temp)
						prev_tag = None
						temp = []
						temp_pos = []
						break
			elif tag[0:2] in ["VB","RB","JJ","TO","DT","IN"] and prev_tag != None and prev_tag[0:2] in ["NN"] and word.lower() not in nltk_stopword_list:
				########### prev word is NOUNE ###############
				if len(temp) > 0:
					result.append(temp)
					prev_tag = None
					temp = []
					temp_pos = []
				temp.append((word,tag))
				temp_pos.append(tag[0:2])	
				prev_tag = tag
			elif tag[0:2] in ["VB","RB","JJ","TO","DT","IN"] and word.lower() not in nltk_stopword_list:
				temp.append((word,tag))
				temp_pos.append(tag[0:2])	
				prev_tag = tag
			elif tag[0:2] in ["DT","TO","IN"] and word.lower() not in nltk_stopword_list and count < len(data) -1 and data[count+1][1][0:2] in ["VB","RB","JJ","TO","DT","IN"]:
				temp.append((word,tag))
				temp_pos.append(tag[0:2])	
				prev_tag = tag
			elif tag[0:2] in ["CC"] and word.lower() not in nltk_stopword_list and count < len(data) -1 and data[count+1][1][0:2] in ["VB","RB","JJ","TO","DT","IN"]:
				if len(temp) > 0:
					result.append(temp)
					prev_tag = None
					temp = []
					temp_pos = []
				temp.append((word,tag))
				temp_pos.append(tag[0:2])	
				prev_tag = tag
			elif len(temp) > 0 and self.validate_opinion(temp):
				if len(temp) > 0:
					result.append(temp)
				prev_tag = None
				temp = []
				temp_pos = []
			elif len(temp) > 0:
				temp = []
				temp_pos = []
				prev_tag = None
			count  = count + 1

		if len(temp) > 0 and self.validate_opinion(temp):
				result.append(temp)
						
		return result

if __name__=="__main__":
	obj = Rule.getInstance()
	data = [('He', 'PRP'), ('and', 'CC'), ('his', 'PRP$'), ('staff', 'NN'), ('were', 'VBD'), ('neither', 'DT'), ('good', 'JJ'), ('nor', 'CC'), ('smart', 'JJ'), ('.', '.')]
	feature = obj.extract_opinion(data)
	print feature
			
