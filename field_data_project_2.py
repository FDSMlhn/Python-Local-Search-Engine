import os 
import sys
import string
import pandas as pd
import numpy as np
import re
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
	y=re.sub(r"[\(\)]",r" ",y)
	if not isinstance(x,set):
		x=re.sub(r"[\(\)]",r" ",x)
		x=[word.strip(string.punctuation).lower() for word in x.split()]
	y_tm=[word.strip(string.punctuation).lower() for word in y.split()]
	return set(x) | set(y_tm)


# word_list=list(reduce(word,dw_texts))

word_list=list(filter(None,list(reduce(word,dw_texts))))



def passage_2_word(x):
	x=re.sub(r"[\(\)]",r" ",x)
	return list(filter(None,[word.strip(string.punctuation).lower() for word in x.split()]))


word_passage = [passage_2_word(x) for x in dw_texts]
frequency_table = []

for i in word_passage:
	frequency_table.append([i.count(k) for k in word_list])
for i in frequency_table:
	i.append(sum(i))
word_list.append("TOTAL NUM OF WORDS IN PASSAGE")

#print(len(word_list))
#print(txt_list)
# for k in word_list:
# 	if len(k)==0:
# 		print("hah{}haha".format(k))
# print(repr(word_list[0]))
# print(repr(word_list[1]))

data = pd.DataFrame(frequency_table,columns=word_list)
F= ((data.drop(data.columns[-1],axis=1)).transpose()/data[data.columns[-1]]).transpose()
DW=data.drop(data.columns[-1],axis=1).applymap(lambda x:x>0).sum()
IDF = np.log(data.shape[0]/DW)
Weight_table = F * IDF
# print(len(k))
# print(k)
#frequncy table
data.to_csv(os.path.join(PATH, "frequency_table.csv"),index=False)
Weight_table.to_csv(os.path.join(PATH, "weight_table.csv"),index=False)

# print(len(word_list))
# print(string.punctuation)
# print("queen's".strip("'"))
