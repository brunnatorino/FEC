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

df = df_initial.copy()

mapping_Valuation = {" Valuation on": " Évaluation sur"}
mapping_ValReverse ={" Valuation on Reverse":" Évaluation sur Contre Passation"}
mapping_ReversePosting = {" Reverse Posting":" Contre Passation d'Ecriture -  Conversion de devise sur 20181026"}
mapping_Translation = {" Translation Using 20181026":" Conversion de devise sur 20181026"}





df = df.replace({"EcritureLib":mapping_Valuation}, regex=True)
