import pandas as pd

df_initial = pd.read_excel('2019journal.xlsx', names =['EcritureDate','Posting Period','Fiscal Year','PieceDate','Document Number',
                                                      'JournalLib','Offsetting','Document Type','CompanyCode','CompteNum','Tax code',
                                                      'Idevise','Amount?','Localcurrency','Montant','UScurrency','MontantUS','EcritureLib','Parked by',
                                                      'User name','Cost Center','Trading Parter'])

del df_initial['Posting Period']
del df_initial['Document Type']
del df_initial['Tax code']
del df_initial['Fiscal Year']
del df_initial['Parked by']
del df_initial['Cost Center']
del df_initial['User name']

## match offsetting account numbers and create a lettering match such as AA, BB, etc...



df = df_initial.copy()

df_dict = {k:v for k,v in df.groupby('JournalLib')}
print(df_dict)

df1 = df[(df['JournalLib']=='FC valuation')]
df1 = df[(df['JournalLib']=='1120181026020000100000')]
df1 = df[(df['JournalLib']=='1120181026020000217020')]
df1 = df[(df['JournalLib']=='Reverse posting')]
df1 = df[(df['JournalLib']=='3120181026010000600900')]
df1 = df[(df['JournalLib']=='3120181026010000600500')]
df1 = df[(df['JournalLib']=='3120181026010000600510')]

df1 = df[(df['JournalLib']=='3120181026010000600770')]

df1 = df[(df['JournalLib']=='3120181026010000600900')]
df1 = df[(df['JournalLib']=='3120181026010000635010')]
df1 = df[(df['JournalLib']=='3120181026010000635030')]
df1 = df[(df['JournalLib']=='3120181026010000644020')]
df1 = df[(df['JournalLib']=='3120181026010000645000')]

df1 = df[(df['JournalLib']=='3120181026010000645010')]
df1 = df[(df['JournalLib']=='3120181026010000645000')]
df1 = df[(df['JournalLib']=='3120181026010000645000')]
