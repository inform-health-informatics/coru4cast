import numpy as np
import pandas as pd

# Load data; check size
df_raw = pd.read_csv('data_raw/SteveH_wardtransfers_pseudonymised.csv')
assert df_raw.shape == (894887, 14)

# Data dictionary
# ===============

df_raw.columns
# AdmissionMethodCode
# -------------------


# see https://www.datadictionary.nhs.uk/data_dictionary/attributes/a/add/admission_method_de.asp?shownav=1

# Elective admissions
# 11 Waiting list
# 12 Booked
# 13 Planned

# Emergency Admission
# 21 via local A&E
# 22 GP referral
# 2A other A&E transfer
# 2B other hospital transfer

# Maternity
# 31 Ante-partum
# 32 Post-partum

# Other
# 81 Tranfers (non emergency)

# TransferType

# TransferNumber
# TransferStartDate
# TransferEndDate

# FacilityCode

# SiteCode
# --------
# RRV03 : UCLH
dict_sitecode = {'RRV03': 'UCLH'}


# WardCode
# --------
df_raw['WardCode'].head()

# Bed
# ---
df_raw['Bed'].head()

# ConsultantCode_Source
df_raw['ConsultantCode_Source'].head()

# SubSpecialtyCode
df_raw['SubSpecialtyCode'].head()




# Inspect distribition of admission types
df_raw['AdmissionMethodCode'].head()




# Types of admissions
df[df['TransferType'] == 'A'].groupby('AdmissionMethodCode')['AdmissionMethodCode'].agg(['count'])
wards = df.groupby('WardCode')['AdmissionMethodCode'].agg(['count'])
# wards.to_clipboard(sep='\t')
df.shape



# So let's produce a focused data set
# Let's focus specifically on UCLH
df = df_raw[df_raw['SiteCode'] == 'RRV03']
df.shape

# Relevant columns
cols = [
    'Spell_pseudo',
    'SiteCode',
    'FacilityCode',
    'AdmissionMethodCode',
    'TransferType',
    'TransferNumber',
    'TransferStartDate',
    'TransferEndDate',
    'WardCode',
    'Bed'
    ]



df = df[cols]
df.rename(columns = {'Spell_pseudo':'pid'},inplace=True)

# Convert to timestamps
df['TransferStartDate'] = pd.to_datetime(df['TransferStartDate'])
df['TransferEndDate'] = pd.to_datetime(df['TransferEndDate'])
df.info()

# Appropriate sorting
df = df.sort_values(['pid', 'SiteCode', 'TransferNumber'])
df.head()

# Now label each pid with min tranfer numbers
dft = (df.groupby('pid')['TransferNumber'].min() == 1).to_frame()
dft.columns = ['minTransferIsOne']
dfr = pd.merge(df, dft, left_on='pid', right_index=True, how='left')
df = dfr

# Cleaning and prep
# =================
# Find complete chains
# - Define clean episodes
#     - Complete trace from 1 to max
#     - Check that the discharge time stamps are duplicates
#     - Check there are no gaps between stop and start
# - Collapse over wards
# - Work out what to do with very short episodes

# Now label each pid with distinct transfer numbers
dft = df.groupby('pid').agg({'TransferNumber': ['nunique', 'max', 'min']})
dft.columns = ['nunique', 'max', 'min']
dft['NoTransfersMissing'] = dft['nunique'] == (dft['max'] - dft['min'] + 1)
dft.loc[:,['NoTransfersMissing']]
dfr = pd.merge(df, dft.loc[:,['NoTransfersMissing']], left_on='pid', right_index=True, how='left')
df = dfr

# inspect
pd.crosstab(df.minTransferIsOne, df.NoTransfersMissing)
these_cols = ['pid', 'TransferType', 'TransferNumber', 'TransferStartDate', 'TransferEndDate']
df[df['NoTransfersMissing'] == False].loc[:,these_cols].head(20)


# - [ ] @TODO: (2018-12-07) @fixme: problem with missing transfers : drop for now
# ditto drop those where we don't observe the start
df = df[df['minTransferIsOne'] == True]
df = df[df['NoTransfersMissing'] == True]
pd.crosstab(df.minTransferIsOne, df.NoTransfersMissing)
df.drop(['minTransferIsOne', 'NoTransfersMissing'], axis=1, inplace=True)

# check that discharge timestamps are dups
dft = df[df['TransferType'] == 'D'][df['TransferStartDate'] != df['TransferEndDate']]
assert dft.shape[0] == 0



#     - Check there are no gaps between stop and start
df = df.sort_values(['pid', 'SiteCode', 'TransferNumber'])
# df['TransferEndDate_L1'] = df.groupby('pid')['TransferEndDate'].shift(1)
df['TransferEndDate_L1'] = df.groupby('pid')['TransferEndDate'].shift(1)
these_cols.append('TransferEndDate_L1')
df['TransferGap'] = df['TransferStartDate'] - df['TransferEndDate_L1']
these_cols.append('TransferGap')
df[these_cols].head()
df.groupby('TransferType')['TransferGap'].describe()

# - [ ] @TODO: (2018-12-07) @resume
# now label up episodes with transfer gaps and inspect

