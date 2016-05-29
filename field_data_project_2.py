import os 
import sys
import string
from functools import reduce

PATH = os.getcwd()
file_path = PATH + "/dw_field_data"
txt_list = os.listdir(file_path)[1:]
txt_path_list = [os.path.join(file_path,k) for k in txt_list]

dw_texts=[]
for i in txt_path_list:
	with open(i,"r") as filename:
		dw_texts.append(filename.read())

def word(x,y):
	if not isinstance(x,set):
		x=[word.strip(string.punctuation).lower() for word in x.split()]
	y_tm=[word.strip(string.punctuation).lower() for word in y.split()]
	return set(x) | set(y_tm)
word_list=list(reduce(word,dw_texts))

dw_texts

print(len(word_list))
print(string.punctuation)
print("queen's".strip("'"))
