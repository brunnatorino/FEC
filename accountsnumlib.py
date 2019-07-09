import pandas as pd
from datetime import datetime, date


file = pd.read_excel("2FEC-reportingMayJune.xlsx")

dictaccounts = pd.read_excel("mapping-accounts.xlsx")

dict1 = dictaccounts[['G/L Account #','FrMap']]
dict2 = dictaccounts[['G/L Account #','FrName']]
dict3 = dictaccounts[['G/L Account #','Name']]

dict1 = dictaccounts.set_index('G/L Account #').to_dict()['FrMap']
dict2 = dictaccounts.set_index('G/L Account #').to_dict()['FrAcc']

file['CompteNum_FR'] = file['CompteNum'].map(dict1).astype(str) + file['CompteNum'].astype(str) 
file['CompteLib_FR'] = file['CompteNum'].replace(dict2)
print(file['CompteNum_FR'])
print(file['CompteLib_FR'])

df1 = pd.read_excel("3FEC-reporting-MayJune.xlsx")
dict4 = dictaccounts[['FrAcc','FrName']]
dict4 = dictaccounts.set_index('FrAcc').to_dict()['FrName']
df1['CompteLib_FR'] = df1['CompteLib_FR'].replace(dict4)
print(df1['CompteLib_FR'].head())

dict5 = dictaccounts[['G/L Account #','Name']]
dict5 = dictaccounts.set_index('G/L Account #').to_dict()['Name']
df1['CompteLib_EN'] = df1['CompteNum'].replace(dict5)
print(df1['CompteLib_EN'].head())

writer = pd.ExcelWriter("5FEC-reporting-MayJune.xlsx",
                        engine='xlsxwriter',
                        datetime_format='yyyymmdd',
                        date_format='yyyymmdd')

df1.to_excel(writer, sheet_name = ('Sheet1'))

workbook  = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_column('B:C', 20)
writer.save()
