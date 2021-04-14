
import re
import os
import sys
from pathlib import Path
import pandas as pd


args = sys.argv[1]
path = Path().cwd()
file = path.joinpath(f"cricket/{args}")

with open('./cricket/001.txt','r',encoding='utf-8') as f:
    data = [x.strip().lower() for x in f if x.strip()]
    data= [re.sub('[^a-z -]+','',x) for x in data]
    data = [' '.join([y for y in x.split() if y]) for x in data]
print(' '.join(data))