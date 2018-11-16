import pandas as pd
import os
import json
import csv

directory = os.fsencode('/home/rohitgpt/ml/box-office-knowledge-discovery/data-collection/movies/')
root = "/home/rohitgpt/ml/box-office-knowledge-discovery/data-collection/movies/"
count = 0
big_list = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"): 
        #print(filename)
        with open(root+filename, "r") as read_file:
            data = json.load(read_file)
            df_temp = pd.DataFrame.from_dict(data,orient='index')
            df_temp = df_temp.T
            big_list.append(df_temp)
        count = count + 1
        #print("#",count,"#")
        if(count%1000==0):
            print("#",count,"#")
        continue
    else:
        continue

print("Files added : ",count)
xx = pd.concat(big_list,sort=False,ignore_index=True)
xx.to_csv('file1.csv',sep='\t',index=False)
