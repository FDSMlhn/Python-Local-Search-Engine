import os 
import sys
import pandas as pd
import numpy as np
from stemming.porter2 import stem
try: 
	KW = sys.argv[1:]
	if not KW:
		raise ValueError
except:
 	print("Please enter some keywords here!")
 	exit(1)


PATH = os.getcwd()
data_path = os.path.join(PATH, "stem_weight_table_wf.csv")
file_path = PATH + "/dw_field_data"
txt_list = os.listdir(file_path)[1:]
datasource = pd.read_csv(data_path)
KW = [stem(i.lower()) for i in KW]
num = None
for j,i in enumerate(KW):
	if i in datasource.columns:
		if num is None:
			num=datasource[i]
			continue
		else:
			num=num+datasource[i]
#outcome = pd.DataFrame(num.rank(method='min')).applymap(lambda x:x>1).order()
#print(outcome)
#value = zip(list(num.rank(method='min'))[outcome], txt_list[outcome])
#print(value)

#print()		
num_ad= list(num)
num_ad = [num_ad[i] + num_ad[i+int(len(num_ad)/2)] for i in range(0,int(len(num_ad)/2))]

outcome = sorted([x for x in num_ad if x > 0],reverse=True)
if len(outcome) >=5:
	outcome = outcome[:5]
for i,entry in enumerate(outcome):
	print("Rank {}:{}.".format(i+1,txt_list[num_ad.index(entry)]))



#def check():




#def preparation():
