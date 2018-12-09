import numpy as np
import pandas as pd

# Load data; check size
df = pd.read_csv('data/transfers.csv')
df.columns
df.drop(['Unnamed: 0'], inplace=True, axis=1)
df.shape

# dft = df.iloc[:10000,:]
dft = df
dft = dft[dft['TransferNumber'] <= 5]
dft.shape
these_cols = ['eid', 'TransferNumber', 'TransferStartDate', 'TransferEndDate']
dups = dft.duplicated(subset=these_cols)
dft = dft[dups == False]

R = dft.pivot(
    index='eid',
    columns='TransferNumber',
    values=['TransferStartDate', 'TransferEndDate', 'WardCode'])
R.head()
R.shape
