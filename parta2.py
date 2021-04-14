import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig1 = sys.argv[0]
fig2 = sys.argv[0]

# fig1 = sys.argv[1]
# fig2 = sys.argv[2]

rawpath = Path().cwd()

df = pd.read_csv(rawpath.joinpath('owid-covid-data (1).csv'))


df['month'] = df['date'].apply(lambda x: pd.Period(f"{'-'.join(x.split('-')[:2])}"))
df['year'] = df['date'].apply(lambda x: f"{pd.Period(x).year}")


mode1 = [np.max]
mode = [np.sum]



newdf = df[df['year'] == '2020'].groupby([ 'month','location'])[
    ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']].aggregate(
    {
        "total_cases": mode1,
        "new_cases": mode,
        "total_deaths": mode1,
        "new_deaths": mode
    }
)

newdf1 = df[df['year'] == '2020'].groupby(['location'])[
    ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']].aggregate(
    {
        "total_cases": mode1,
        "new_cases": mode,
        "total_deaths": mode1,
        "new_deaths": mode
    }
)

# print(newdf1.shape)
### cdr
newdf1.insert(newdf1.shape[1], 'case_datality_rate', newdf1['total_deaths']['amax'] / newdf1['total_cases']['amax'])
# print(newdf1)


plt.figure()
plt.xscale('symlog')
plt.scatter(newdf1['new_cases']['sum'], newdf1['case_datality_rate'])

plt.savefig(f"{fig1.split('.')[0]}.jpg")
plt.show()

### plot 2

plt.figure()
plt.scatter(newdf1['new_cases']['sum'].apply(np.log10), newdf1['case_datality_rate'])

# plt.savefig(f"{fig2.split('.')[0] }.jpg")
plt.savefig(f"{fig2.split('.')[0] + '1'}.jpg")
plt.show()
