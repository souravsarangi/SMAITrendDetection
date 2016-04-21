#!/usr/bin/env python
import re
import operator
from tokendef import *
import datetime
from nltk.corpus import treebank
from nltk import stem
stemmer=stem.PorterStemmer()

def addelement(element):
	element = element.lower()
	element = re.sub(r"(?:\@|https?\://)\S+", "", element)
	if element != ' ' and element!='' :
		if element not in stopwords:
			#tokens.append(stemmer.stem_word(element))
			tokens.append((element))
	

def checkforshortforms(inputtext, inputtextnext, i, flag):
	if flag == 0:
		pattern = re.compile(r"^([A-Z]\.)+$")
		if re.match(pattern, inputtext):
			addelement(inputtext)
			return 1
		return 0
	return 1

def processmainstring(textinput):
	for i in gapsadder:
		textinput.replace(i,' ')
	for i in remover:
		textinput.replace(i,'')
	return textinput



def checkforfullstops(inputtext, flag):
	if flag == 0:
		pattern = re.compile(r'[.]+$')
		if(re.search(pattern, inputtext)):
			inputtext = inputtext.replace(re.search(pattern, inputtext).group(), ' '+ re.search(pattern, inputtext).group())
			inputtext = inputtext.split()
			for i in range(0,len(inputtext)):
				addelement(inputtext[i])
			return 1
		return 0
	return 1

def handlegaps(textinput):
	pattern = re.compile(r"\s+")
	textinput = re.sub(pattern, " ", textinput)
	return textinput

def check_date(textinput,flag):
	if flag==0:
	  try:
	    if datetime.datetime.strptime(textinput, '%Y.%m.%d'):
	    	tokens.append(textinput)
	    return 1
	  except ValueError:
	    return 0
	return 1
'''def check_url(textinput,flag):
	if flag==0:
		if()'''	

def preprocess(textinput):
	textinput = textinput.decode('unicode_escape').encode('ascii','ignore')
	textinput = processmainstring(textinput)
	textinput = handlegaps(textinput)
	return textinput



def process(textinput):
	textinput = textinput.split(" ")
	for i in xrange(0,len(textinput)):
		if(len(textinput[i]) > 0):
			flag = 0
			try:
				flag = checkforshortforms(textinput[i],textinput[i+1],i,flag)
			except:
				flag = checkforshortforms(textinput[i],"is",i,flag)
			flag = checkforfullstops(textinput[i],flag)
			flag = check_date(textinput[i],flag)
			if(flag == 0):
				addelement(textinput[i])




def tokenise(text):
	global tokens
	global tokendictionary
	tokens = []
	line = text.rstrip('\n')
	if len(line)!= 0:
			line = preprocess(line)
			process(line)
	return tokens