#!/usr/bin/env python
# coding: utf-8

from scipy.io import loadmat
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

rel_path = '../' # suppose that py file lies in ~/src/

mat_arr = loadmat(rel_path + 'data/imdb_crop/imdb.mat')['imdb']

urls = mat_arr['full_path'][0][0][0]
urls = list(map(lambda url: rel_path+'data/imdb_crop/'+url[0], urls))

photo_taken = mat_arr['photo_taken'][0][0][0]

dob = mat_arr['dob'][0][0][0]

year_to_subtr = []
broken_idx = []

for i, matlab_datenum in enumerate(dob):
    try:
        dt = timedelta(days=int(matlab_datenum) -366) + datetime(1,1,1)
        dt_arr = list(dt.timetuple())
        year = dt_arr[0]

        # suppose that photo was taken at 1 of July
        if dt_arr[1] == 7:
            if dt_arr[2] > 1:
                year += 1
        if dt_arr[1] > 7:
            year += 1
        year_to_subtr.append(year)
    except:
        print("broken matlab serial number:", i,  matlab_datenum)
        broken_idx.append(i)
    if (i % 10000) == 0:
         print("record", i+1, "processed, successfully parsed", len(year_to_subtr), 'years... ')

urls = np.delete(urls,broken_idx)

photo_taken = np.delete(photo_taken,broken_idx)

ages = list(map(lambda taken, yob: taken - yob, photo_taken, year_to_subtr))

def age_to_clusters(age):
    if age < 25:
        return 0
    if age > 48:
        return 1
    return 2

clusters = list(map(age_to_clusters, ages))

result = {}
result['urls'] = urls
result['age_clusters'] = clusters
result['ages'] = ages

df = pd.DataFrame(result, index=None)
print(df.shape)

with open(rel_path+'csv/total.csv', mode='w', encoding='utf-8') as f_csv:
    df.to_csv(f_csv)
