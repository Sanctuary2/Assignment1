import re
import os
import sys
from pathlib import Path
import pandas as pd
from itertools import chain

args = sys.argv[1:]
path = Path().cwd()
filepath = path.joinpath('./cricket')
files = [filepath.joinpath(x) for x in os.listdir(filepath)]

docid = pd.read_csv(path.joinpath('partb1.csv'),sep='\t')

result = []
for file in files:
    with open(file,'r',encoding='utf-8') as f:
        data = [x.strip().lower() for x in f if x.strip()]
        data= [re.sub('[^a-z -]+','',x) for x in data]
        data = [[y for y in x.split() if y] for x in data]
        data = set(chain(*data))


    if set(args) & data == set(args):
        result.extend(docid[docid['filename'] == file.name].documentID.values.tolist())

print(result)
