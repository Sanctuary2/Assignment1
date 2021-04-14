
import re
import os
import sys
from pathlib import Path
import pandas as pd


args = sys.argv[1]
path = Path().cwd()
filepath = path.joinpath('./cricket')
files = [filepath.joinpath(x) for x in os.listdir(filepath)]
idcompile = re.compile('[A-Z]+-[0-9]+[a-zA-Z]*')

result = {'filename':[],'documentID':[]}
for file in files:
    with open(file,'r',encoding='utf-8') as f:
        data = [x.strip() for x in f if x.strip()]
    data = ' '.join(data)
    for x in re.finditer(idcompile,data):
        result['filename'].append(file.name)
        result['documentID'].append(x.group())
pd.DataFrame(result).to_csv(args,sep='\t',index=False)
pd.DataFrame(result).to_excel(f"{args.split('.')[0]+'.xlsx'}")