from asyncore import read
import glob
import json
import pandas as pd

files = sorted(glob.glob('data/crawl/USDT_ETH/*.json'))

_all_data = []
for f in files:
    with open(f) as _f:
        _all_data.extend(json.loads(_f.read()))

df = pd.DataFrame(_all_data)
df.rename(columns={
    'date': 'Date',
    'high': 'High',
    'low': 'Low',
    'open': 'Open',
    'close': 'Close',
    'volume': 'Volume'
},
          inplace=True)
df.drop(['quoteVolume'], axis=1, inplace=True)
df.drop(['weightedAverage'], axis=1, inplace=True)

# with open("all.csv", 'w+', encoding='utf-8') as _file:
df.to_csv("all.csv", index=False)