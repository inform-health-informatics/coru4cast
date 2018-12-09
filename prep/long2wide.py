import numpy as np
import pandas as pd

# Load data; check size
df = pd.read_csv('data/transfers.csv')
maskCol = [
    'eid', 'TransferType', 'TransferNumber', 'WardCode', 'Bed',
    'TransferStartDate', 'TransferEndDate'
 ]

# Discharge Transfers do not represent a 'path' so label then drop
# df['discharged'] = df.groupby('eid')['TransferType'].transform(lambda x: 'D' in x.values)
df = df.assign(discharged=df.TransferType.eq('D').groupby(df.eid).transform('any'))
# maskRow = df.TransferType != 'D'
# df = df[maskRow]
maskCol.append('discharged')
df[maskCol]

# collapse over ward level movements
# identify within episodes where prev ward is the same
df['WardCode_L1'] = df.groupby('eid')['WardCode'].shift(1)
maskCol.append('WardCode_L1')
df.WardCode_L1.value_counts(dropna=False)
df['TransferInternal'] = False
maskRow = df.WardCode == df.WardCode_L1
df.loc[maskRow, 'TransferInternal'] = True
df.TransferInternal.value_counts()

maskCol.append('TransferInternal')

# define mask to keep admissions, discharge events, between ward transfers
maskRow = (df.TransferType == 'A') | (df.TransferType == 'D') | (
    (df.TransferType == 'T') & (df.TransferInternal == False))

# Manual visual inspection and check
df[df.eid == 5086][maskCol]
df[maskRow][df.eid == 5086][maskCol]

df = df[maskRow]
# now drop TransferEndDate since this only represents the bed transfer
df.drop(
    ['TransferEndDate', 'TransferInternal', 'WardCode_L1', 'Bed'],
    inplace=True, axis=1)
df['TransferEndDate'] = np.nan
df = df.sort_values(['eid', 'TransferStartDate'])
df['TransferEndDate'] = df.groupby('eid')['TransferStartDate'].shift(-1)

df.columns
maskCol = [
    'eid', 'TransferType', 'TransferNumber', 'WardCode',
    'TransferStartDate', 'TransferEndDate', 'AdmissionType',
    'AdmissionMethodCode'
 ]

df[maskCol].head()
df[maskRow][df.eid == 5086][maskCol]

# Now create a new 'ward' transfer number
df.rename({'TransferNumber': 'BedTransferNumber'}, inplace=True)
df['TransferNumber'] = df.groupby('eid').cumcount()

# replace final ward with 'discharged'
df.loc[df.TransferType == 'D', 'WardCode'] = 'discharged'



# dft = df.iloc[:10000,:]
dft = df
dft = dft[dft['TransferNumber'] <= 5]
dft.shape
# these_cols = ['eid', 'TransferNumber', 'TransferStartDate', 'TransferEndDate']
# dups = dft.duplicated(subset=these_cols)
# dft = dft[dups == False]

R = dft.pivot(
    index='eid',
    columns='TransferNumber',
    values=['TransferStartDate', 'TransferEndDate', 'WardCode'])
R.shape
R[9100:9120]
