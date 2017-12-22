#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 
import json

# get reviews in Las Vegas
data = pd.read_csv('/Users/qcat/las_vegas_new.csv')
idx = list(data['business_id'])
paper = []
los = []
with open('/Users/qcat/Downloads/dataset/review.json','r') as fo:    
    for line in fo:  
        if (json.loads(line)['business_id'] in idx):#determine if the review is in the city
            try: 
                los.append(json.loads(line))    
            except ValueError:            
                continue
# save Las vegas review file
#df = pd.DataFrame(los)
#df.to_csv('~/los_review.csv', index=False)

# filter resteraunts reviews
data = pd.read_csv('/Users/qcat/las_vegas_cate.csv')
cate = list(data['categories'])
b_idx = list(data['business_id'])
restaurant = []
for i in range(len(cate)):
    if ('Restaurants' in cate[i]):
        restaurant.append(b_idx[i])

#lv_data = pd.read_csv('~/los_review.csv')
lv_data = pd.DataFrame(los)
idx = list(lv_data['business_id'])
lv_res = []
listLV = lv_data.values.tolist()
for j in range(len(idx)) :
    if idx[j] in restaurant:
        lv_res.append(listLV[j])

# save Las vegas restaurant review file
df = pd.DataFrame(lv_res)
df.to_csv('~/las_rest_review.csv', index=False)