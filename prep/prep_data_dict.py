import pandas as pd

# see https://datadictionary.nhs.uk/data_dictionary/attributes/a/add/admission_method_de.asp?shownav=1
# via http://www.datadictionary.wales.nhs.uk/index.html#!WordDocuments/admissionmethod.htm

"""
Value   Type    Meaning Valid From  Valid To
11  Elective Admission  Waiting list    Pre 28th December 1995
12  Elective Admission  Booked  Pre 28th December 1995
13  Elective Admission  Planned Pre 28th December 1995
14  Elective Admission  Activity under the Welsh Assembly Government 2nd Offer Scheme (Originating Provider)    1st April 2006
15  Elective Admission  Activity under the Welsh Assembly Government 2nd Offer Scheme (Receiving Provider)  1st April 2006
21  Emergency Admission A & E or dental casualty department of the health care provider Pre 28th December 1995
22  Emergency Admission GP: after a request for immediate admission has been made direct to a hospital provider (i.e. not through a Bed Bureau) by a General Practitioner or deputy Pre 28th December 1995
23  Emergency Admission Bed bureau  Pre 28th December 1995
24  Emergency Admission Consultant clinic of this or another health care provider   Pre 28th December 1995
25  Emergency Admission Domiciliary visit by Consultant     30th June 1997
27  Emergency Admission Via NHS Direct Services 1st September 2001
28  Emergency Admission Other means, including admitted from the A & E department of another provider where they had not been admitted  Pre 28th December 1995
31  Maternity Admission Admitted ante-partum    Pre 28th December 1995
32  Maternity Admission Admitted post-partum    Pre 28th December 1995
81  Other   Transfer of any admitted patient from other hospital provider.  May be used for an elective or emergency transfer from other hospital provider. Pre 28th December 1995
82  Other   The birth of a baby in this health care provider    Pre 28th December 1995
83  Other   Baby born outside the health care provider (except when born at home as intended.  In this case the baby is an emergency admission.  e.g. if midwife's decision to admit the baby use Admission Method 28)  Pre 28th December 1995
98  Other   Not Applicable  1st May 1998    20th January 2002
99  Other   Not Known   Pre 28th December 1995  20th January 2002
"""
# copy above; maybe via Excel
x = pd.read_clipboard()
x.columns
x.info()
x.to_csv('data_raw/admission_code.csv')
