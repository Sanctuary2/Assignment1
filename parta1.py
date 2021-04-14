import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

args = sys.argv[1]

rawpath = Path().cwd()

df = pd.read_csv(rawpath.joinpath('owid-covid-data (1).csv'))

df['month'] = df['date'].apply(lambda x: pd.Period(f"{'-'.join(x.split('-')[:2])}"))
df['year'] = df['date'].apply(lambda x: f"{pd.Period(x).year}")

mode1 = [np.max]
mode = [np.sum]


newdf = df[df['year'] == '2020'].groupby(['location', 'month'])[
    ['total_cases', 'new_cases', 'total_deaths', 'new_deaths']].aggregate(
    {
        "total_cases": mode1,
        "new_cases": mode,
        "total_deaths": mode1,
        "new_deaths": mode
    }
)


newdf.insert(newdf.shape[1], 'case_datality_rate', newdf['total_deaths']['amax'] / newdf['total_cases']['amax'])


print(newdf.head(5))



newdf.to_csv(rawpath.joinpath(f'{args}'))
newdf.to_excel(rawpath.joinpath(f"{args.split('.')[0] + '.xlsx'}"))