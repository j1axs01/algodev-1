#!/usr/local/bin/python3
from nltk import sent_tokenize, word_tokenize,pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.stem import WordNetLemmatizer
from nltk import *
from nltk.corpus import stopwords
import collections
import os
import findtype as f
import re
import pickle
import argparse
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktLanguageVars

def parse_args():
	parser=argparse.ArgumentParser( description ='supply stopword,pattern, directory of the files')
	parser.add_argument('--stopword',required=True)
	parser.add_argument('--pattern',required=True)
	parser.add_argument('--directory',required=True)
	return parser.parse_args()


def sentence_former(stopword,pattern,filename):
	class BulletPointLangVars(PunktLanguageVars):
		sent_end_chars = ( '.',':','\x0C')
	finallist = []
	tokenizer = PunktSentenceTokenizer(lang_vars = BulletPointLangVars())
	stop_words = set(stopwords.words('english'))
	total_dict={}
	flag = stopword
	counter = 0
	subject='Misc'
	punkt_param = PunktParameters()
	fo = open(filename,'r',encoding='ISO-8859-1')
	fotext = fo.read()
	filetext = re.sub(r'(\n{1,})(s*[a-z])',r' \2',fotext)
	filetext = re.sub(r'([^\.])(\n{1,})(\s*[a-z])',r' \3',filetext)
	filetext = re.sub(r'\n{2,}|\r{2,}|[\x0C]|\:(\W[A-Za-z]+)+','. ',filetext,flags=re.MULTILINE)
	for s in tokenizer.tokenize(filetext):
		counter = counter + 1
		total_dict[counter]=s
	for key, value in total_dict.items():
		value = re.sub(r'[-+]?\d*\.\d+', '-',value)
		value = re.sub(r'[\x00-\x1f\x7f-\x9f]','',value)
		value = re.sub(r'\s*\.\s*','.',value)
		value = re.sub(r'\s$','', value)
		value = re.sub(r'\s{2,}', ' ', value)
		value = re.sub(r'\d+\:\d+','',value)
		value = re.sub(r'\s*\.','\.',value)
		value = re.sub(r'[^a-zA-Z\s\.]+','',value)
		if re.search(pattern, value.strip(),re.I):
			#print(filename,value)
			k=0
			word_list = []
			empty_list = [os.path.basename(filename), value]
			#print("######################################################################")
			for i in re.split(pattern,value):
				title = 'preffix' if k % 2 == 0 else 'suffix'
				k= k+1
				wc = 0
				word_tokens = pos_tag(word_tokenize(i))
				word_tokens.reverse() if k % 2 != 0 else None
				for w in word_tokens:
					word_list.append([wc,w])
					wc = wc + 1
				empty_list.append([title,word_list])
			#print(empty_list)
			finallist.append(empty_list)
	return(finallist)
def main():
	args = parse_args()
	totallist = []
	for subdirs, dirs, files in os.walk(args.directory):
		for file in files:
			filepath = subdirs+'/'+file
			filename = filepath
			totallist.append(sentence_former(args.stopword, args.pattern, filename)) if len(sentence_former(args.stopword, args.pattern, filename)) != 0 else None
	print(totallist)

if __name__ == "__main__":
	main()
