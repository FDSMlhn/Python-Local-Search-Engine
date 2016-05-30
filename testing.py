import os 
import sys
import pandas as pd
import numpy as np

try: 
	KW = sys.argv[1:]
	if not KW:
		raise ValueError
except:
 	print("Please enter some keywords here!")
 	exit(1)

PATH = os.getcwd()
data_path = os.path.join(PATH, "weight_table.csv")
file_path = PATH + "/dw_field_data"
txt_list = os.listdir(file_path)[1:]

datasource = pd.read_csv(data_path)

num=None
for i in KW:
	if i in datasource.columns and not num:
		num = datasource[i]
	else:
		num +=datasource[i]
		
num_ad= list(num)
outcome = sorted([x for x in num_ad if x > 0],reverse=True)
for i,entry in enumerate(outcome):
	print(num_ad.index(entry))
	print("Rank {}:{}.".format(i+1,txt_list[num_ad.index(entry)]))


#def check():




#def preparation():
