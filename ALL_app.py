## joins document numbers if they are not in already (most important piece of code for sequentiality AND balance of accounts)

import pandas as pd
GL = pd.read_excel("GL.xlsx")
ENTRY = pd.read_excel("ENTRY.xlsx")
DELETED = pd.read_excel("DELETED.xlsx")

numbers = GL['Document Number'].tolist()
GL = GL.append(ENTRY[~ENTRY['Document Number'].isin(numbers)])


import pandas as pd
from datetime import datetime, date

## Write File name and input name of the colums 

print("Hello. Let's start! This notebook has many cells that start with []: on the left side on the screen.")
print("Each of them contain the script that will help you in the FEC file for France")
print("Each cell has a description of what it does, starting with ##")
print("                                                              ")
print("IMPORTANT: Before starting, make sure that your file (or a copy of) is in the folder downloads")
print("To run the cell press the play button in the upper part of this window")
print("To answer the questions the cell asks you, just press enter")
print("For the best possible formatting, run the cells chronologically as they show in this notebook")
print("                                                              ")
print("Some cells may ask you questions! Please answer them to continue the cell operation")
print("Make sure that you put the name of the file here:")
print("                                                              ")
file = input("Name of the file:")
df = pd.read_excel(file)
print("                                                              ")
print("Below is the first five excel cells of the file you selected:")
print(df.head())
print("                                                              ")
print("PS: If the program is taking more than a minute, go to tab Kernel and press shutdown all kernels")
print("If the dot on the right side of the window is black, it means that python is working on your request")

a,b,c,d,e,f,g,h,i,j,k = input("Name of column with the document types: "),input("Name of column with doc.header text: "),input("Name of column with document number: "),input("Name of column with entry date: "),input("Name of column with account number: "),input("Name of column with account name,enter NA if does not exist yet: "),input("Name of column with vendor numbers, offsetting acc. no: "),input("Name of column with vendor names, enter NA if it does not exist yet: "),input("Name of column with reference numbers: "),input("Name of columns with document date: "),input("Name of column with text description of the entry: ")

df['EcritureLib'] = df[k]
df['JournalLib'] = df[b]

## MAPPING OF VENDORS FROM THE OFFSETTING ACCOUNTS / FROM FAGLL03 ENTRY VIEW 

vendors = pd.read_excel("Vendors1.xlsx")
df['CompAuxLib'] = df[g]

vendors = vendors.set_index('No').to_dict()['Name']
df['CompAuxLib'] = df['CompAuxLib'].map(vendors)
df['CompAuxNum'] = "F" + df['CompAuxLib']

print("Vendor numbers and names were successfully matched!")
print("Please note the new columns will be called CompAuxLib and CompAuxNum and will be at the end of the excel sheet")

## MAPPING OF DOC HEADER TEXTS AND FILLING OF EMPTY VALUES

journals = pd.read_excel("test128.xlsx")
codes = pd.read_excel('mapping-journal.xlsx')
journals = journals.set_index('DocHeader').to_dict()['JournalLib_FR']
codes = codes.set_index('JournalCode').to_dict()["JournalLib_FR"]

df['JournalCode'] = df[a]
df.loc[df["JournalLib"].isnull(),'JournalLib'] = df["JournalCode"].map(str)
df['JournalLib'] = df['JournalLib'].replace(journals)
df['JournalLib'] = df['JournalLib'].replace(codes)

## Replacing blanks in the Text column with the doc header + vendor name cells if they are not blank, and doc header text + account name if they are
## Replacing reference column with journal code + document number if blank 

df['PieceRef'] = df[i]
df['EcritureNum'] = df[c]
df['EcritureDate'] = df[d]

for row in df['EcritureLib'].isnull():
    df.loc[~df["CompAuxLib"].isnull(),'EcritureLib'] = df['JournalLib'].map(str) + " de " + df['CompAuxLib'].map(str)
    df.loc[df["CompAuxLib"].isnull(),'EcritureLib'] = df['JournalLib'].map(str) + df['EcritureNum'].map(str)
    
df.loc[df["PieceRef"].isnull(),'PieceRef'] = df["JournalCode"].map(str) + df['EcritureNum'].map(str)



print("The column text was successfully filled! Preference was given to vendor names with doc. header text when available. If not, row was filled with")
print("account name and doc. header text")
print("Reference column was sucessfully filled! Format used was journal code and document number")

## creating translated columns for the excel sheet 

mapping_Valuation = {" Valuation on": " Évaluation sur"," Valuation on Reverse":" Évaluation sur Contre Passation",
                     " Reverse Posting":" Contre-Passation d'Ecriture -  Conversion de devise sur",
                     " Translation Using":" Conversion de devise sur"}
mapping_AA = {"Reclass from": " Reclassification de", "reclass from": " Reclassification de", "ZEE MEDIA":"ZEE MEDIA Campaignes Numériques", "TRAINING CONTRI. ER JANUARY '19":"FORMATION CONTRI. ER JANVIER' 19",
              "TAX FEES":"Taxes","SOCIAL SECURITY: URSSAF":"SÉCURITÉ SOCIALE: URSSAF","SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÉCURITÉ SOCIALE: CONTRIBUTIONS À LA FORMATION",
              "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÉCURITÉ SOCIALE: CONTRIBUTION À L’APPRENTISSAGE","RSM":"SERVICES DE PAIE RSM EF18","RSA":"SERVICES DE PAIE RSA OCT-JAN",
              "PRIVATE HEALTH":"SANTÉ PRIVÉE: ASSURANCE MÉDICALE-AXA/","PENSION: PENSION CONTRIBUTIONS - REUNICA":"PENSION: COTISATIONS DE RETRAITE-REUNICA","PENSION: LIFE & DISABILITY INSURANCE - R":"PENSION: ASSURANCE VIE & INVALIDITÉ-R", 
              "PENSION JANUARY '19":"PENSION JANVIER '19",
              "ON CALL JANUARY '19":"Disponible Janvier'19",
              "NRE + PROJECT INITIATION FEES":"NRE + FRAIS D’INITIATION AU PROJET (PO 750003","NET PAY JANUARY '19":"Payeante Janvier'19","JANUARY'19":"JANVIER'19",
              "LUNCH VOUCHER- WITHHOLDING":"BON DÉJEUNER-RETENUE","HOLIDAY BONUS ACCRUAL FY18/19":"CUMUL DES PRIMES DE VACANCES EF18/19",
              "GROSS SALARY JANUARY '19":"SALAIRE BRUT JANVIER' 19","EMEA ACCRUAL P8FY19":"P8FY19 D’ACCUMULATION EMEA","COMMISSION RE-ACCRUAL":"COMMISSION RÉ-ACCUMULATION",
              "COMMISSION ACCRUAL":"COMMISSION D’ACCUMULATION","MARCH":"MARS","MAY":"MAI","APRIL":"AVRIL","AUDIT FEES":"HONORAIRES D’AUDIT",
              "UNSUBMITTED_UNPOSTED BOA ACCRUAL":"Accumulation BOA non soumise non exposée","UNASSIGNED CREDITCARD BOA ACCRUAL":"NON ASSIGNÉ CREDITCARD BOA ACCUMULATION ",
              "EMEA ACCRUAL":"ACCUMULATION EMEA","Exhibit Expenses":"Frais d'exposition","Hotel Tax":"Taxe hôtelière","Company Events":"Événements d'entreprise",
              "Public Transport":"Transport public", "Agency Booking Fees":"Frais de réservation d'agence","Working Meals (Employees Only)":"Repas de travail (employés seulement)",
              "Airfare":"Billet d'avion","Office Supplies":"Fournitures de bureau","Tolls":"Péages",
              "write off difference see e-mail attached":"radiation de la différence voir e-mail ci-joint",
             "Manual P/ment and double payment to be deduct":"P/ment manuel et double paiement à déduire","FX DIFFERENCE ON RSU":"DIFFERENCE FX SUR RSU",
             "DEFINED BENEFIT LIABILITY-TRUE UP":"RESPONSABILITÉ À PRESTATIONS DÉTERMINÉES-TRUE UP","EXTRA RELEASE FOR STORAGE REVERSED":"EXTRA LIBERATION POUR STOCKAGE CONTREPASSATION",
             "RECLASS BANK CHARGES TO CORRECT COST CEN":"RECLASSER LES FRAIS BANCAIRES POUR CORRIGER","PAYROLL INCOME TAXES":"IMPÔTS SUR LES SALAIRES",
              "TRAINING TAX TRUE UP":"TAXE DE FORMATION", "FX DIFFERENCE ON STOCK OPTION EXERCISES":"FX DIFFERENCE SUR LES EXERCICES D'OPTIONS STOCK",
              "Airline Frais":"Frais de Transport Aérien","Agency Booking Fees":"Frais de Réservation d'Agence","Computer Supplies":"Fournitures informatiques",
             "AUDIT FEES":"FRAIS D'AUDIT", "HOLIDAY BONUS ACCRUAL ":"ACCUMULATION DE BONUS DE VACANCES","TAX FEES":"FRAIS D'IMPÔT",
              "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÉCURITÉ SOCIALE: CONTRIBUITION À L’APPRENTISSAGE",
              "SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÉCURITÉ SOCIALE: CONTRIBUTIONS À LA FORMATION", "TRAVEL COST":"FRAIS DE VOYAGE", "HOUSING TAX":"TAXE SUR LE LOGEMENT", 
             "PAYROLL INCOME TAXES":"IMPÔTS SUR LE REVENU DE LA PAIE","INCOME TAX-PAS":"IMPÔT SUR LE REVENU-PAS", "IC SETTLEMENT":"Règlement Interentreprises",
             "VACATION TAKEN":"VACANCES PRISES", "SOCIAL SECURITY: APPR. CONTR.":"SÉCURITÉ SOCIALE: CONTRIBUTION À L’APPRENTISSAGE", 
              "POST OF AVRIL DEC IN CORRECT SIGN":"CORRECTION D'ECRITURE AVRIL DEC"}



df = df.replace({"EcritureLib":mapping_Valuation}, regex=True)
df = df.replace({"EcritureLib":mapping_AA}, regex=True)

df['EcritureLib'] = df["EcritureLib"].str.replace('COST-PLUS', 'Revient Majoré')
df['EcritureLib'] = df["EcritureLib"].str.replace('PRITVAE HEALTH: MEDICAL INSURANCE', 'SANTÉ PRIVÉE: ASSURANCE MÉDICALE')
df['EcritureLib'] = df["EcritureLib"].str.replace('MEDICAL INSURANCE', 'ASSURANCE MÉDICALE')
df['EcritureLib'] = df["EcritureLib"].str.replace('UNASSIGNED', 'NON ATTRIBUÉ')
df['EcritureLib'] = df["EcritureLib"].str.replace('Payout', 'Paiement')
df['EcritureLib'] = df["EcritureLib"].str.replace('FRINGE COST', 'COÛT MARGINAL')
df['EcritureLib'] = df["EcritureLib"].str.replace('PROJECT INITIATION', 'LANCEMENT DU PROJET')
df['EcritureLib'] = df["EcritureLib"].str.replace('ACCRUAL', 'ACCUMULATION')
df['EcritureLib'] = df["EcritureLib"].str.replace('CREDITCARD', 'CARTE DE CRÉDIT')
df['EcritureLib'] = df["EcritureLib"].str.replace('ACCR ', 'ACCUM ')
df['EcritureLib'] = df["EcritureLib"].str.replace('VAT ', 'TVA ')
df['EcritureLib'] = df["EcritureLib"].str.replace('SOCIAL SECURITY ', 'SÉCURITÉ SOCIALE')
df['EcritureLib'] = df["EcritureLib"].str.replace('SEPTEMBER', 'SEPT')
df['EcritureLib'] = df["EcritureLib"].str.replace('TAXBACK', 'Reboursement')
df['EcritureLib'] = df["EcritureLib"].str.replace('REPORT', '')
df['EcritureLib'] = df["EcritureLib"].str.replace("Reverse Posting", "Contre Passation d'Ecriture")
df['EcritureLib'] = df["EcritureLib"].str.replace("BASE RENT", "Location Base")
df['EcritureLib'] = df["EcritureLib"].str.replace("Rent ", "Location ")
df['EcritureLib'] = df["EcritureLib"].str.replace("RENT ", "Location ")
df['EcritureLib'] = df["EcritureLib"].str.replace("CLEARING", "compensation ")
df['EcritureLib'] = df["EcritureLib"].str.replace("clearing", "compensation ")
df['EcritureLib'] = df["EcritureLib"].str.replace("BILLING CHARGES", "FRAIS DE FACTURATION ")
df['EcritureLib'] = df["EcritureLib"].str.replace("UNPAID", "NON PAYÉ")
df['EcritureLib'] = df["EcritureLib"].str.replace("PROPERTY TAX", "IMPÔT FONCIER ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Trans. Using", "Conversion sur")
df['EcritureLib'] = df["EcritureLib"].str.replace("SALARIES", "Salaires")
df['EcritureLib'] = df["EcritureLib"].str.replace("Refund", "Remboursement")
df['EcritureLib'] = df["EcritureLib"].str.replace("REFUND", "Remboursement")
df['EcritureLib'] = df["EcritureLib"].str.replace("no invoice", "pas de facture")
df['EcritureLib'] = df["EcritureLib"].str.replace("COST-PLUS SERVICE REVENUE", "Revenus de service Revient Majoré")
df['EcritureLib'] = df["EcritureLib"].str.replace("SETTLEMENT", "RÈGLEMENT ")
df['EcritureLib'] = df["EcritureLib"].str.replace("PURCHASE", "ACHAT")
df['EcritureLib'] = df["EcritureLib"].str.replace("NON-CP SETTLE", "RÈGLEMENT NON-CP")
df['EcritureLib'] = df["EcritureLib"].str.replace("PAID ", " Payé ")
df['EcritureLib'] = df["EcritureLib"].str.replace("FEES ", "Frais")

df['EcritureLib'] = df["EcritureLib"].str.replace("January", "Janvier")
df['EcritureLib'] = df["EcritureLib"].str.replace("February", "Février")
df['EcritureLib'] = df["EcritureLib"].str.replace("March", "Mars")
df['EcritureLib'] = df["EcritureLib"].str.replace("April", "Avril")
df['EcritureLib'] = df["EcritureLib"].str.replace("May", "Mai")
df['EcritureLib'] = df["EcritureLib"].str.replace("June", "Juin")
df['EcritureLib'] = df["EcritureLib"].str.replace("July", "Juillet")
df['EcritureLib'] = df["EcritureLib"].str.replace("September", "Septembre")
df['EcritureLib'] = df["EcritureLib"].str.replace("Aug.", "Août")

df['EcritureLib'] = df["EcritureLib"].str.replace("JANUARY", "Janvier")
df['EcritureLib'] = df["EcritureLib"].str.replace("FEBRUARY", "Février")
df['EcritureLib'] = df["EcritureLib"].str.replace("MARCH", "Mars")
df['EcritureLib'] = df["EcritureLib"].str.replace("APRIL", "Avril")
df['EcritureLib'] = df["EcritureLib"].str.replace("MAY", "Mai")
df['EcritureLib'] = df["EcritureLib"].str.replace("JUNE", "Juin")
df['EcritureLib'] = df["EcritureLib"].str.replace("JULY", "Juillet")
df['EcritureLib'] = df["EcritureLib"].str.replace("SEPTEMBER", "Septembre")
df['EcritureLib'] = df["EcritureLib"].str.replace("AUGUST.", "Août")
df['EcritureLib'] = df["EcritureLib"].str.replace("NOVEMBER.", "Novembre")
df['EcritureLib'] = df["EcritureLib"].str.replace("DECEMBER.", "Décembre")
df['EcritureLib'] = df["EcritureLib"].str.replace("December", "Décembre")

df['EcritureLib'] = df["EcritureLib"].str.replace("Feb.", "Fév.")
df['EcritureLib'] = df["EcritureLib"].str.replace("Mar.", "Mars")
df['EcritureLib'] = df["EcritureLib"].str.replace("Apr.", "Avril")
df['EcritureLib'] = df["EcritureLib"].str.replace("Aug.", "Août")
df['EcritureLib'] = df["EcritureLib"].str.replace("Aug.", "Août")
df['EcritureLib'] = df["EcritureLib"].str.replace("Reverse ", "Contre-passation ")

df['EcritureLib'] = df["EcritureLib"].str.replace("INTEREST CHARGE", "CHARGE D'INTÉRÊT")
df['EcritureLib'] = df["EcritureLib"].str.replace("-SICK LEAVE PAY", "-Paiement congé maladie")
df['EcritureLib'] = df["EcritureLib"].str.replace("RECLASSEMENTIFICATION", "RECLASSIFICATION")
df['EcritureLib'] = df["EcritureLib"].str.replace("INSTALMENT", "VERSEMENT")
df['EcritureLib'] = df["EcritureLib"].str.replace("FIRST", "1ere")
df['EcritureLib'] = df["EcritureLib"].str.replace("FINE LATE PAY.", "Amende pour retard de paiement")
df['EcritureLib'] = df["EcritureLib"].str.replace("-PATERNITY PAY", "Indemnités de paternité")
df['EcritureLib'] = df["EcritureLib"].str.replace("SOCIAL SECURITY:", "SÉCURITÉ SOCIALE:")
df['EcritureLib'] = df["EcritureLib"].str.replace("Trip from", "Voyage de:")
df['EcritureLib'] = df["EcritureLib"].str.replace(" To ", " à")
df['EcritureLib'] = df["EcritureLib"].str.replace("Shipping", "Livraison")
df['EcritureLib'] = df["EcritureLib"].str.replace("VOXEET INTEGRATION COSTS", "COÛTS D'INTÉGRATION DE VOXEET")
df['EcritureLib'] = df["EcritureLib"].str.replace("INCOME TAX", "IMPÔT SUR LE REVENU")
df['EcritureLib'] = df["EcritureLib"].str.replace('Rideshare', 'Covoiturage')
df['EcritureLib'] = df["EcritureLib"].str.replace('Travel Meals', 'Repas de Travail')
df['EcritureLib'] = df["EcritureLib"].str.replace('Fees', 'Frais')
df['EcritureLib'] = df["EcritureLib"].str.replace('Phone', 'Téléphone')
df['EcritureLib'] = df["EcritureLib"].str.replace("Books", "Abonnements")
df['EcritureLib'] = df["EcritureLib"].str.replace("Subcriptions", "Location Base")
df['EcritureLib'] = df["EcritureLib"].str.replace("Meals", "Repas")
df['EcritureLib'] = df["EcritureLib"].str.replace("Entertainment", "divertissement ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Third Party", "tiers ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Training Fees", "Frais d0 Formation")
df['EcritureLib'] = df["EcritureLib"].str.replace("Conferences/Tradeshows Registratio", "Conférences/Tradeshows Enregistrement")
df['EcritureLib'] = df["EcritureLib"].str.replace("FOR", "POUR")
df['EcritureLib'] = df["EcritureLib"].str.replace("ROUNDING", "ARRONDISSEMENT")
df['EcritureLib'] = df["EcritureLib"].str.replace("STORAGE", "STOCKAGE")
df['EcritureLib'] = df["EcritureLib"].str.replace("VACATION ACCURAL", "Vacances Accumulées")
df['EcritureLib'] = df["EcritureLib"].str.replace("RECEIVABLE ", "Recevables")
df['EcritureLib'] = df["EcritureLib"].str.replace("AFTER PAYOUT ", "APRÈS PAIEMENT")
df['EcritureLib'] = df["EcritureLib"].str.replace("CLEAN UP ", "APUREMENT")
df['EcritureLib'] = df["EcritureLib"].str.replace("EMPLOYEE TRAVEL INSUR ", "ASSURANCE DE VOYAGE DES EMPLOYÉS")
df['EcritureLib'] = df["EcritureLib"].str.replace("CORRECTION OF", "CORRECTION DE")
df['EcritureLib'] = df["EcritureLib"].str.replace("TAXES PAYROLL", "IMPÔTS SUR LA MASSE SALARIALE")
df['EcritureLib'] = df["EcritureLib"].str.replace("ACCOUNT", "COMPTE")
df['EcritureLib'] = df["EcritureLib"].str.replace("TAX", "Impôt")
df['EcritureLib'] = df["EcritureLib"].str.replace("life disab", "Incapacité de vie")
df['EcritureLib'] = df["EcritureLib"].str.replace("HOUSING TAX","TAXE D'HABITATION")
df['EcritureLib'] = df["EcritureLib"].str.replace("GROSS SALARY","SALAIRE BRUT")
df['EcritureLib'] = df["EcritureLib"].str.replace("Cleaning Services","Nettoyage")
df['EcritureLib'] = df["EcritureLib"].str.replace("Freight","Fret")
df['EcritureLib'] = df["EcritureLib"].str.replace("Membership","adhésion")
df['EcritureLib'] = df["EcritureLib"].str.replace("Air cooling Maintenance","Entretien de refroidissement de l'air")
df['EcritureLib'] = df["EcritureLib"].str.replace("Power on Demand Platform","Plateforme d'energie à la demande")
df['EcritureLib'] = df["EcritureLib"].str.replace("Sanitaire room installation"," Installation de la salle sanitaire")
df['EcritureLib'] = df["EcritureLib"].str.replace("subscription","abonnement")
df['EcritureLib'] = df["EcritureLib"].str.replace("Coffee supplies "," Fournitures de café")
df['EcritureLib'] = df["EcritureLib"].str.replace("Duty and Tax ","Devoir et fiscalité")
df['EcritureLib'] = df["EcritureLib"].str.replace("Electricity ","Electricité ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Lunch vouchers  ","Bons déjeuner")
df['EcritureLib'] = df["EcritureLib"].str.replace("Security monitoring","Surveillance de la sécurité")
df['EcritureLib'] = df["EcritureLib"].str.replace("Water", "L'EAU")
df['EcritureLib'] = df["EcritureLib"].str.replace("Statutory Audit", "Audit statutaire")
df['EcritureLib'] = df["EcritureLib"].str.replace(" Meeting room screen installation", "Installation de l'écran de la salle de réunion")
df['EcritureLib'] = df["EcritureLib"].str.replace("Water", "L'EAU")
df['EcritureLib'] = df["EcritureLib"].str.replace("Water", "L'EAU")
df['EcritureLib'] = df["EcritureLib"].str.replace("Tax Credit FY 2016", "Crédit d'impôt Exercice 2016")
df['EcritureLib'] = df["EcritureLib"].str.replace("Bank of America Merill Lynch-T&E statement","Déclaration de Merill Lynch")
df['EcritureLib'] = df["EcritureLib"].str.replace("English Translation", "Traduction anglaise")
df['EcritureLib'] = df["EcritureLib"].str.replace("Office Rent", "Location de Bureau")

df['EcritureLib'] = df["EcritureLib"].str.replace("Annual Electrical Verification", "Vérification électrique annuelle ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Health costs ", "Coûts santé")
df['EcritureLib'] = df["EcritureLib"].str.replace("Unlimited-receipt and policy audit", "Vérification illimitée des reçus et audites")
df['EcritureLib'] = df["EcritureLib"].str.replace("Water fountain ", "Fontaine d'eau")
df['EcritureLib'] = df["EcritureLib"].str.replace("Quartely control visit", "Visite de contrôle trimestrielle")
df['EcritureLib'] = df["EcritureLib"].str.replace("Fire extinguishers annual check", "Vérification annuelle des extincteurs")
df['EcritureLib'] = df["EcritureLib"].str.replace("showroom rent", "location de salle d'exposition")
df['EcritureLib'] = df["EcritureLib"].str.replace("AND ACTUAL RECEIV","ET RECETTES RÉELLES")
df['EcritureLib'] = df["EcritureLib"].str.replace("FILING","DÉPÔT")
df['EcritureLib'] = df["EcritureLib"].str.replace("ORDERS","ORDRES")
df['EcritureLib'] = df["EcritureLib"].str.replace("EXCLUDED -DUMMY CREDIT","EXCLU")
df['EcritureLib'] = df["EcritureLib"].str.replace("RELARING TO","RELATIF À")
df['EcritureLib'] = df["EcritureLib"].str.replace("CLEAN UP-","APUREMENT-")
df['EcritureLib'] = df["EcritureLib"].str.replace("2ND INSTALLEMENT","2ème versement")
df['EcritureLib'] = df["EcritureLib"].str.replace("DOUBLE PAYMENT","DOUBLE PAIEMENT")
df['EcritureLib'] = df["EcritureLib"].str.replace("CLEAN UP-","APUREMENT-")
df['EcritureLib'] = df["EcritureLib"].str.replace("DUTIES","DROITS")
df['EcritureLib'] = df["EcritureLib"].str.replace("Previous balance","Solde Précédent")
df['EcritureLib'] = df["EcritureLib"].str.replace("Cash fx","Cash FX")
df['EcritureLib'] = df["EcritureLib"].str.replace("PAYROLL INCOME","REVENU DE PAIE")
df['EcritureLib'] = df["EcritureLib"].str.replace("TELEPHONE CHARGES","Frais de Téléphone")
df['EcritureLib'] = df["EcritureLib"].str.replace("Clearing","Compensation")
df['EcritureLib'] = df["EcritureLib"].str.replace("Hotel","Hôtel")
df['EcritureLib'] = df["EcritureLib"].str.replace("Miscellaneous","Divers")
df['EcritureLib'] = df["EcritureLib"].str.replace("Corporate Card-Out-of-Poc","")
df['EcritureLib'] = df["EcritureLib"].str.replace("Traveling Dolby Empl","Employé itinérant de Dolby")
df['EcritureLib'] = df["EcritureLib"].str.replace("Tools-Equipment-Lab Supplies","Outils-Equipement-Fournitures de laboratoire")
df['EcritureLib'] = df["EcritureLib"].str.replace("rounding","Arrondissement")
df['EcritureLib'] = df["EcritureLib"].str.replace("Building Supplies-Maintenance","Matériaux de construction-Entretien")
df['EcritureLib'] = df["EcritureLib"].str.replace("Expensed Furniture","Mobilier Dépensé")
df['EcritureLib'] = df["EcritureLib"].str.replace("Credit for Charges","Crédit pour frais")
df['EcritureLib'] = df["EcritureLib"].str.replace("Manual P-ment and double payment to be deduct","P-mnt manuel et double paiement à déduire")
df['EcritureLib'] = df["EcritureLib"].str.replace("Employee insurance travel","Assurance de voyage des employés 2019")
df['EcritureLib'] = df["EcritureLib"].str.replace("Rent ","Location ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Lunch vouchers ","Bons déjeuner")
df['EcritureLib'] = df["EcritureLib"].str.replace("Store Room ","Chambre Stocke")
df['EcritureLib'] = df["EcritureLib"].str.replace("Evaluation ","Évaluation  ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Charges ","Frais ")
df['EcritureLib'] = df["EcritureLib"].str.replace("On Line ","En ligne ")
df['EcritureLib'] = df["EcritureLib"].str.replace("/Building Supplies/Maintenance","/ Matériaux de construction / Entretien")
df['EcritureLib'] = df["EcritureLib"].str.replace("Music Instruments","Instruments Musicales")
df['EcritureLib'] = df["EcritureLib"].str.replace("/Employee Awards/Recognition", "/ Récompenses des employés / Reconnaissance")


df['EcritureLib'] = df["EcritureLib"].str.replace("/Daily Allowance","/Indemnité journalière")

df['EcritureLib'] = df["EcritureLib"].str.replace("RECLASS ", "RECLASSIFICATION ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Purchase Accounting", "Comptabilité d'achat")
df['EcritureLib'] = df["EcritureLib"].str.replace( "EXPAT ", " Expatrié ")
df['EcritureLib'] = df["EcritureLib"].str.replace("FROM ", "DE ")
df['EcritureLib'] = df["EcritureLib"].str.replace("INVOICE", "FACTURE")
df['EcritureLib'] = df["EcritureLib"].str.replace("CLEANUP", "APUREMENT")
df['EcritureLib'] = df["EcritureLib"].str.replace("Repayment", "Restitution")

df['EcritureLib'] = df["EcritureLib"].str.replace("Office Furniture", "Meubles de bureau")
df['EcritureLib'] = df["EcritureLib"].str.replace("anti-stress treatments", "traitements anti-stress")

df['EcritureLib'] = df["EcritureLib"].str.replace("UK Tax Return", "Décl. d'impôt Royaume-Uni")
df['EcritureLib'] = df["EcritureLib"].str.replace("Office Location", "Location de bureau")
df['EcritureLib'] = df["EcritureLib"].str.replace("Deliver Service", "Service de livraison")
df['EcritureLib'] = df["EcritureLib"].str.replace("Foreign Office Support", "Soutien aux bureaux étrangères")
df['EcritureLib'] = df["EcritureLib"].str.replace("Showroom", "Salle d'exposition")

df['EcritureLib'] = df["EcritureLib"].str.replace("aditional Services", "Services supplémentaires ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Cofee consumption Paris office", "Consommation de café Bureau de Paris")

df['EcritureLib'] = df["EcritureLib"].str.replace("Consultant ", "Expert-conseil")
df['EcritureLib'] = df["EcritureLib"].str.replace("INVOICE", "FACTURE")
df['EcritureLib'] = df["EcritureLib"].str.replace("Rent-", "Location-")
df['EcritureLib'] = df["EcritureLib"].str.replace("Corporate", "Entreprise")
df['EcritureLib'] = df["EcritureLib"].str.replace("COST ", "COÛT ")
df['EcritureLib'] = df["EcritureLib"].str.replace("TRAINING", "Formation")
df['EcritureLib'] = df["EcritureLib"].str.replace("LIFE DISAB", "Invalidité")
df['EcritureLib'] = df["EcritureLib"].str.replace("INSU ", "ASSURANCE ")
df['EcritureLib'] = df["EcritureLib"].str.replace("PATENT AWARD", "BREVET")

df['EcritureLib'] = df["EcritureLib"].str.replace("EQUIVALENT POUR UNUSED VACATION POUR LEAVE", "CONGÉ DE VACANCES INUTILISÉS")
df['EcritureLib'] = df["EcritureLib"].str.replace("SPOT ", "")
df['EcritureLib'] = df["EcritureLib"].str.replace("AIRFARE TRANSFER TO PREPAIDS", "TRANSFERT DE TRANSPORT AÉRIEN À PAYÉ D'AVANCE")
df['EcritureLib'] = df["EcritureLib"].str.replace("WITHHOLDING", "RETRAIT")
df['EcritureLib'] = df["EcritureLib"].str.replace("Clear ", "Reglement ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Clear ", "Reglement ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Rent/", "Location/")
df['EcritureLib'] = df["EcritureLib"].str.replace("Pay ", "Paiement ")
df['EcritureLib'] = df["EcritureLib"].str.replace("PAYMENT", "Paiement ")

df['EcritureLib'] = df["EcritureLib"].str.replace("French Income Tax Return;", "Déclaration de revenus française;")
df['EcritureLib'] = df["EcritureLib"].str.replace("REVESERVICES", "SERVICES")
df['EcritureLib'] = df["EcritureLib"].str.replace("INCLUDED DOUBLE", "DOUBLE INCLUS")
df['EcritureLib'] = df["EcritureLib"].str.replace("Bank", "Banque")
df['EcritureLib'] = df["EcritureLib"].str.replace("/Promotional Expenses", "/Frais de promotion")

df['EcritureLib'] = df["EcritureLib"].str.replace(" ACTIVITY ", " activité ")
df['EcritureLib'] = df["EcritureLib"].str.replace(" DEFINED BENEFIT LIABILITY", "PASSIF À AVANTAGES DÉTERMINÉES")
df['EcritureLib'] = df["EcritureLib"].str.replace("COÛT PLUS ", "Revient Majoré")
df['EcritureLib'] = df["EcritureLib"].str.replace("/Airline Frais", "/Tarifs aériens")
df['EcritureLib'] = df["EcritureLib"].str.replace("/Tools/Equipment/Lab Supplies", "/Outils / Équipement / Fournitures de laboratoire")
df['EcritureLib'] = df["EcritureLib"].str.replace("Rent/", "Location/")
df['EcritureLib'] = df["EcritureLib"].str.replace("Payment Posting", "Paiements")
df['EcritureLib'] = df["EcritureLib"].str.replace("COMMISSION D’ACCUMULATION", "ACCUMULATIONS DE COMISSIONS")
df['EcritureLib'] = df["EcritureLib"].str.replace("ImpôtE", "Impôt")
df['EcritureLib'] = df["EcritureLib"].str.replace("MED.INSU", "MED.ASSURANCE")
df['EcritureLib'] = df["EcritureLib"].str.replace("APPRENTICESHIP_CONTRIBUTIONS_TRUE_UP", "CONTRIBUTIONS À L'APPRENTISSAGE/TRUE UP")
df['EcritureLib'] = df["EcritureLib"].str.replace("NET PAY", "SALAIRE NET")
df['EcritureLib'] = df["EcritureLib"].str.replace("CASH ", "ARGENT ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Repayment ", "Repaiement ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Acct. ", "Comptab. ")

df['EcritureLib'] = df["EcritureLib"].str.replace("ACCR ", "ACC ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Accr ", "Acc.")
df['EcritureLib'] = df["EcritureLib"].str.replace("Cash Balance", "Solde de caisse")
df['EcritureLib'] = df["EcritureLib"].str.replace("RECLASS ", "RECLASSEMENT ")
df['EcritureLib'] = df["EcritureLib"].str.replace("VAT FILING ", "Dépôt de TVA ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Needs to be re-booked due", "KI")
df['EcritureLib'] = df["EcritureLib"].str.replace("reclass from", "reclasser de")
df['EcritureLib'] = df["EcritureLib"].str.replace("RECLASS FROM", "reclasser de")
df['EcritureLib'] = df["EcritureLib"].str.replace("PAYROLL", "PAIE")
df['EcritureLib'] = df["EcritureLib"].str.replace("RECLASS ", "Reclasser")

df['EcritureLib'] = df["EcritureLib"].str.replace("DEDICTION","DEDUCTION")
df['EcritureLib'] = df["EcritureLib"].str.replace("Cash","Argent ")
df['EcritureLib'] = df["EcritureLib"].str.replace("cash ","argent ")
df['EcritureLib'] = df["EcritureLib"].str.replace("ReclasserIFICATIO","RECLASSEMENT ")
df['EcritureLib'] = df["EcritureLib"].str.replace("ImpôtS ","Impôts ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Working Repas (Employees Only) ","Repas de travail (employés seulement) ")
df['EcritureLib'] = df["EcritureLib"].str.replace("/Banque Frais","/Frais Bancaires")
df['EcritureLib'] = df["EcritureLib"].str.replace("MED. INS.","ASSURANCE MED.")

mapping_Valuation1 = {" Valuation on": " Évaluation sur"," Valuation on Reverse":" Évaluation sur Contre Passation",
                     " Reverse Posting":" Contre-Passation d'Ecriture -  Conversion de devise sur",
                     " Translation Using":" Conversion de devise sur"}
mapping_AA1 = {"Reclass from": " Reclassification de", "reclass from": " Reclassification de", "ZEE MEDIA":"ZEE MEDIA Campaignes Numériques", "TRAINING CONTRI. ER JANUARY '19":"FORMATION CONTRI. ER JANVIER' 19",
              "TAX FEES":"Taxes","SOCIAL SECURITY: URSSAF":"SÉCURITÉ SOCIALE: URSSAF","SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÉCURITÉ SOCIALE: CONTRIBUTIONS À LA FORMATION",
              "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÉCURITÉ SOCIALE: CONTRIBUTION À L’APPRENTISSAGE","RSM":"SERVICES DE PAIE RSM EF18","RSA":"SERVICES DE PAIE RSA OCT-JAN",
              "PRIVATE HEALTH":"SANTÉ PRIVÉE: ASSURANCE MÉDICALE-AXA/","PENSION: PENSION CONTRIBUTIONS - REUNICA":"PENSION: COTISATIONS DE RETRAITE-REUNICA","PENSION: LIFE & DISABILITY INSURANCE - R":"PENSION: ASSURANCE VIE & INVALIDITÉ-R", 
              "PENSION JANUARY '19":"PENSION JANVIER '19",
              "ON CALL JANUARY '19":"Disponible Janvier'19",
              "NRE + PROJECT INITIATION FEES":"NRE + FRAIS D’INITIATION AU PROJET (PO 750003","NET PAY JANUARY '19":"Payeante Janvier'19","JANUARY'19":"JANVIER'19",
              "LUNCH VOUCHER- WITHHOLDING":"BON DÉJEUNER-RETENUE","HOLIDAY BONUS ACCRUAL FY18/19":"CUMUL DES PRIMES DE VACANCES EF18/19",
              "GROSS SALARY JANUARY '19":"SALAIRE BRUT JANVIER' 19","EMEA ACCRUAL P8FY19":"P8FY19 D’ACCUMULATION EMEA","COMMISSION RE-ACCRUAL":"COMMISSION RÉ-ACCUMULATION",
              "COMMISSION ACCRUAL":"COMMISSION D’ACCUMULATION","MARCH":"MARS","MAY":"MAI","APRIL":"AVRIL","AUDIT FEES":"HONORAIRES D’AUDIT",
              "UNSUBMITTED_UNPOSTED BOA ACCRUAL":"Accumulation BOA non soumise non exposée","UNASSIGNED CREDITCARD BOA ACCRUAL":"NON ASSIGNÉ CREDITCARD BOA ACCUMULATION ",
              "EMEA ACCRUAL":"ACCUMULATION EMEA","Exhibit Expenses":"Frais d'exposition","Hotel Tax":"Taxe hôtelière","Company Events":"Événements d'entreprise",
              "Public Transport":"Transport public", "Agency Booking Fees":"Frais de réservation d'agence","Working Meals (Employees Only)":"Repas de travail (employés seulement)",
              "Airfare":"Billet d'avion","Office Supplies":"Fournitures de bureau","Tolls":"Péages",
              "write off difference see e-mail attached":"radiation de la différence voir e-mail ci-joint",
             "Manual P/ment and double payment to be deduct":"P/ment manuel et double paiement à déduire","FX DIFFERENCE ON RSU":"DIFFERENCE FX SUR RSU",
             "DEFINED BENEFIT LIABILITY-TRUE UP":"RESPONSABILITÉ À PRESTATIONS DÉTERMINÉES-TRUE UP","EXTRA RELEASE FOR STORAGE REVERSED":"EXTRA LIBERATION POUR STOCKAGE CONTREPASSATION",
             "RECLASS BANK CHARGES TO CORRECT COST CEN":"RECLASSER LES FRAIS BANCAIRES POUR CORRIGER","PAYROLL INCOME TAXES":"IMPÔTS SUR LES SALAIRES",
              "TRAINING TAX TRUE UP":"TAXE DE FORMATION", "FX DIFFERENCE ON STOCK OPTION EXERCISES":"FX DIFFERENCE SUR LES EXERCICES D'OPTIONS STOCK",
              "Airline Frais":"Frais de Transport Aérien","Agency Booking Fees":"Frais de Réservation d'Agence","Computer Supplies":"Fournitures informatiques",
             "AUDIT FEES":"FRAIS D'AUDIT", "HOLIDAY BONUS ACCRUAL ":"ACCUMULATION DE BONUS DE VACANCES","TAX FEES":"FRAIS D'IMPÔT",
              "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÉCURITÉ SOCIALE: CONTRIBUITION À L’APPRENTISSAGE",
              "SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÉCURITÉ SOCIALE: CONTRIBUTIONS À LA FORMATION", "TRAVEL COST":"FRAIS DE VOYAGE", "HOUSING TAX":"TAXE SUR LE LOGEMENT", 
             "PAYROLL INCOME TAXES":"IMPÔTS SUR LE REVENU DE LA PAIE","INCOME TAX-PAS":"IMPÔT SUR LE REVENU-PAS", "IC SETTLEMENT":"Règlement Interentreprises",
             "VACATION TAKEN":"VACANCES PRISES", "SOCIAL SECURITY: APPR. CONTR.":"SÉCURITÉ SOCIALE: CONTRIBUTION À L’APPRENTISSAGE", 
              "POST OF AVRIL DEC IN CORRECT SIGN":"CORRECTION D'ECRITURE AVRIL DEC"}



df = df.replace({"JournalLib":mapping_Valuation1}, regex=True)
df = df.replace({"JournalLib":mapping_AA1}, regex=True)

print("Your file was sucessfully translated! Please check the final excel file to adjust any words and/or sentences it may have missed before submitting")

## TRANSLATION OF DOC HEADER TEXTS

df['JournalLib'] = df["JournalLib"].str.replace('COST-PLUS', 'Revient Majoré')
df['JournalLib'] = df["JournalLib"].str.replace('PRITVAE HEALTH: MEDICAL INSURANCE', 'SANTÉ PRIVÉE: ASSURANCE MÉDICALE')
df['JournalLib'] = df["JournalLib"].str.replace('MEDICAL INSURANCE', 'ASSURANCE MÉDICALE')
df['JournalLib'] = df["JournalLib"].str.replace('UNASSIGNED', 'NON ATTRIBUÉ')
df['JournalLib'] = df["JournalLib"].str.replace('Payout', 'Paiement')
df['JournalLib'] = df["JournalLib"].str.replace('FRINGE COST', 'COÛT MARGINAL')
df['JournalLib'] = df["JournalLib"].str.replace('PROJECT INITIATION', 'LANCEMENT DU PROJET')
df['JournalLib'] = df["JournalLib"].str.replace('ACCRUAL', 'ACCUMULATION')
df['JournalLib'] = df["JournalLib"].str.replace('CREDITCARD', 'CARTE DE CRÉDIT')
df['JournalLib'] = df["JournalLib"].str.replace('ACCR ', 'ACCUM ')
df['JournalLib'] = df["JournalLib"].str.replace('VAT ', 'TVA ')
df['JournalLib'] = df["JournalLib"].str.replace('SOCIAL SECURITY ', 'SÉCURITÉ SOCIALE')
df['JournalLib'] = df["JournalLib"].str.replace('SEPTEMBER', 'SEPT')
df['JournalLib'] = df["JournalLib"].str.replace('TAXBACK', 'Reboursement')
df['JournalLib'] = df["JournalLib"].str.replace('REPORT', '')
df['JournalLib'] = df["JournalLib"].str.replace("Reverse Posting", "Contre Passation d'Ecriture")
df['JournalLib'] = df["JournalLib"].str.replace("BASE RENT", "Location Base")
df['JournalLib'] = df["JournalLib"].str.replace("Rent ", "Location ")
df['JournalLib'] = df["JournalLib"].str.replace("RENT ", "Location ")
df['JournalLib'] = df["JournalLib"].str.replace("CLEARING", "compensation ")
df['JournalLib'] = df["JournalLib"].str.replace("clearing", "compensation ")
df['JournalLib'] = df["JournalLib"].str.replace("BILLING CHARGES", "FRAIS DE FACTURATION ")
df['JournalLib'] = df["JournalLib"].str.replace("UNPAID", "NON PAYÉ")
df['JournalLib'] = df["JournalLib"].str.replace("PROPERTY TAX", "IMPÔT FONCIER ")
df['JournalLib'] = df["JournalLib"].str.replace("Trans. Using", "Conversion sur")
df['JournalLib'] = df["JournalLib"].str.replace("SALARIES", "Salaires")
df['JournalLib'] = df["JournalLib"].str.replace("Refund", "Remboursement")
df['JournalLib'] = df["JournalLib"].str.replace("REFUND", "Remboursement")
df['JournalLib'] = df["JournalLib"].str.replace("no invoice", "pas de facture")
df['JournalLib'] = df["JournalLib"].str.replace("COST-PLUS SERVICE REVENUE", "Revenus de service Revient Majoré")
df['JournalLib'] = df["JournalLib"].str.replace("SETTLEMENT", "RÈGLEMENT ")
df['JournalLib'] = df["JournalLib"].str.replace("PURCHASE", "ACHAT")
df['JournalLib'] = df["JournalLib"].str.replace("NON-CP SETTLE", "RÈGLEMENT NON-CP")
df['JournalLib'] = df["JournalLib"].str.replace("PAID ", " Payé ")
df['JournalLib'] = df["JournalLib"].str.replace("FEES ", "Frais")

df['JournalLib'] = df["JournalLib"].str.replace("January", "Janvier")
df['JournalLib'] = df["JournalLib"].str.replace("February", "Février")
df['JournalLib'] = df["JournalLib"].str.replace("March", "Mars")
df['JournalLib'] = df["JournalLib"].str.replace("April", "Avril")
df['JournalLib'] = df["JournalLib"].str.replace("May", "Mai")
df['JournalLib'] = df["JournalLib"].str.replace("June", "Juin")
df['JournalLib'] = df["JournalLib"].str.replace("July", "Juillet")
df['JournalLib'] = df["JournalLib"].str.replace("September", "Septembre")
df['JournalLib'] = df["JournalLib"].str.replace("Aug.", "Août")

df['JournalLib'] = df["JournalLib"].str.replace("JANUARY", "Janvier")
df['JournalLib'] = df["JournalLib"].str.replace("FEBRUARY", "Février")
df['JournalLib'] = df["JournalLib"].str.replace("MARCH", "Mars")
df['JournalLib'] = df["JournalLib"].str.replace("APRIL", "Avril")
df['JournalLib'] = df["JournalLib"].str.replace("MAY", "Mai")
df['JournalLib'] = df["JournalLib"].str.replace("JUNE", "Juin")
df['JournalLib'] = df["JournalLib"].str.replace("JULY", "Juillet")
df['JournalLib'] = df["JournalLib"].str.replace("SEPTEMBER", "Septembre")
df['JournalLib'] = df["JournalLib"].str.replace("AUGUST.", "Août")
df['JournalLib'] = df["JournalLib"].str.replace("NOVEMBER.", "Novembre")
df['JournalLib'] = df["JournalLib"].str.replace("DECEMBER.", "Décembre")
df['JournalLib'] = df["JournalLib"].str.replace("December", "Décembre")

df['JournalLib'] = df["JournalLib"].str.replace("Feb.", "Fév.")
df['JournalLib'] = df["JournalLib"].str.replace("Mar.", "Mars")
df['JournalLib'] = df["JournalLib"].str.replace("Apr.", "Avril")
df['JournalLib'] = df["JournalLib"].str.replace("Aug.", "Août")
df['JournalLib'] = df["JournalLib"].str.replace("Aug.", "Août")
df['JournalLib'] = df["JournalLib"].str.replace("Reverse ", "Contre-passation ")

df['JournalLib'] = df["JournalLib"].str.replace("INTEREST CHARGE", "CHARGE D'INTÉRÊT")
df['JournalLib'] = df["JournalLib"].str.replace("-SICK LEAVE PAY", "-Paiement congé maladie")
df['JournalLib'] = df["JournalLib"].str.replace("RECLASSEMENTIFICATION", "RECLASSIFICATION")
df['JournalLib'] = df["JournalLib"].str.replace("INSTALMENT", "VERSEMENT")
df['JournalLib'] = df["JournalLib"].str.replace("FIRST", "1ere")
df['JournalLib'] = df["JournalLib"].str.replace("FINE LATE PAY.", "Amende pour retard de paiement")
df['JournalLib'] = df["JournalLib"].str.replace("-PATERNITY PAY", "Indemnités de paternité")
df['JournalLib'] = df["JournalLib"].str.replace("SOCIAL SECURITY:", "SÉCURITÉ SOCIALE:")
df['JournalLib'] = df["JournalLib"].str.replace("Trip from", "Voyage de:")
df['JournalLib'] = df["JournalLib"].str.replace(" To ", " à")
df['JournalLib'] = df["JournalLib"].str.replace("Shipping", "Livraison")
df['JournalLib'] = df["JournalLib"].str.replace("VOXEET INTEGRATION COSTS", "COÛTS D'INTÉGRATION DE VOXEET")
df['JournalLib'] = df["JournalLib"].str.replace("INCOME TAX", "IMPÔT SUR LE REVENU")
df['JournalLib'] = df["JournalLib"].str.replace('Rideshare', 'Covoiturage')
df['JournalLib'] = df["JournalLib"].str.replace('Travel Meals', 'Repas de Travail')
df['JournalLib'] = df["JournalLib"].str.replace('Fees', 'Frais')
df['JournalLib'] = df["JournalLib"].str.replace('Phone', 'Téléphone')
df['JournalLib'] = df["JournalLib"].str.replace("Books", "Abonnements")
df['JournalLib'] = df["JournalLib"].str.replace("Subcriptions", "Location Base")
df['JournalLib'] = df["JournalLib"].str.replace("Meals", "Repas")
df['JournalLib'] = df["JournalLib"].str.replace("Entertainment", "divertissement ")
df['JournalLib'] = df["JournalLib"].str.replace("Third Party", "tiers ")
df['JournalLib'] = df["JournalLib"].str.replace("Training Fees", "Frais d0 Formation")
df['JournalLib'] = df["JournalLib"].str.replace("Conferences/Tradeshows Registratio", "Conférences/Tradeshows Enregistrement")
df['JournalLib'] = df["JournalLib"].str.replace("FOR", "POUR")
df['JournalLib'] = df["JournalLib"].str.replace("ROUNDING", "ARRONDISSEMENT")
df['JournalLib'] = df["JournalLib"].str.replace("STORAGE", "STOCKAGE")
df['JournalLib'] = df["JournalLib"].str.replace("VACATION ACCURAL", "Vacances Accumulées")
df['JournalLib'] = df["JournalLib"].str.replace("RECEIVABLE ", "Recevables")
df['JournalLib'] = df["JournalLib"].str.replace("AFTER PAYOUT ", "APRÈS PAIEMENT")
df['JournalLib'] = df["JournalLib"].str.replace("CLEAN UP ", "APUREMENT")
df['JournalLib'] = df["JournalLib"].str.replace("EMPLOYEE TRAVEL INSUR ", "ASSURANCE DE VOYAGE DES EMPLOYÉS")
df['JournalLib'] = df["JournalLib"].str.replace("CORRECTION OF", "CORRECTION DE")
df['JournalLib'] = df["JournalLib"].str.replace("TAXES PAYROLL", "IMPÔTS SUR LA MASSE SALARIALE")
df['JournalLib'] = df["JournalLib"].str.replace("ACCOUNT", "COMPTE")
df['JournalLib'] = df["JournalLib"].str.replace("TAX", "Impôt")
df['JournalLib'] = df["JournalLib"].str.replace("life disab", "Incapacité de vie")
df['JournalLib'] = df["JournalLib"].str.replace("HOUSING TAX","TAXE D'HABITATION")
df['JournalLib'] = df["JournalLib"].str.replace("GROSS SALARY","SALAIRE BRUT")
df['JournalLib'] = df["JournalLib"].str.replace("Cleaning Services","Nettoyage")
df['JournalLib'] = df["JournalLib"].str.replace("Freight","Fret")
df['JournalLib'] = df["JournalLib"].str.replace("Membership","adhésion")
df['JournalLib'] = df["JournalLib"].str.replace("Air cooling Maintenance","Entretien de refroidissement de l'air")
df['JournalLib'] = df["JournalLib"].str.replace("Power on Demand Platform","Plateforme d'energie à la demande")
df['JournalLib'] = df["JournalLib"].str.replace("Sanitaire room installation"," Installation de la salle sanitaire")
df['JournalLib'] = df["JournalLib"].str.replace("subscription","abonnement")
df['JournalLib'] = df["JournalLib"].str.replace("Coffee supplies "," Fournitures de café")
df['JournalLib'] = df["JournalLib"].str.replace("Duty and Tax ","Devoir et fiscalité")
df['JournalLib'] = df["JournalLib"].str.replace("Electricity ","Electricité ")
df['JournalLib'] = df["JournalLib"].str.replace("Lunch vouchers  ","Bons déjeuner")
df['JournalLib'] = df["JournalLib"].str.replace("Security monitoring","Surveillance de la sécurité")
df['JournalLib'] = df["JournalLib"].str.replace("Water", "L'EAU")
df['JournalLib'] = df["JournalLib"].str.replace("Statutory Audit", "Audit statutaire")
df['JournalLib'] = df["JournalLib"].str.replace(" Meeting room screen installation", "Installation de l'écran de la salle de réunion")
df['JournalLib'] = df["JournalLib"].str.replace("Water", "L'EAU")
df['JournalLib'] = df["JournalLib"].str.replace("Water", "L'EAU")
df['JournalLib'] = df["JournalLib"].str.replace("Tax Credit FY 2016", "Crédit d'impôt Exercice 2016")
df['JournalLib'] = df["JournalLib"].str.replace("Bank of America Merill Lynch-T&E statement","Déclaration de Merill Lynch")
df['JournalLib'] = df["JournalLib"].str.replace("English Translation", "Traduction anglaise")
df['JournalLib'] = df["JournalLib"].str.replace("Office Rent", "Location de Bureau")

df['JournalLib'] = df["JournalLib"].str.replace("Annual Electrical Verification", "Vérification électrique annuelle ")
df['JournalLib'] = df["JournalLib"].str.replace("Health costs ", "Coûts santé")
df['JournalLib'] = df["JournalLib"].str.replace("Unlimited-receipt and policy audit", "Vérification illimitée des reçus et audites")
df['JournalLib'] = df["JournalLib"].str.replace("Water fountain ", "Fontaine d'eau")
df['JournalLib'] = df["JournalLib"].str.replace("Quartely control visit", "Visite de contrôle trimestrielle")
df['JournalLib'] = df["JournalLib"].str.replace("Fire extinguishers annual check", "Vérification annuelle des extincteurs")
df['JournalLib'] = df["JournalLib"].str.replace("showroom rent", "location de salle d'exposition")
df['JournalLib'] = df["JournalLib"].str.replace("AND ACTUAL RECEIV","ET RECETTES RÉELLES")
df['JournalLib'] = df["JournalLib"].str.replace("FILING","DÉPÔT")
df['JournalLib'] = df["JournalLib"].str.replace("ORDERS","ORDRES")
df['JournalLib'] = df["JournalLib"].str.replace("EXCLUDED -DUMMY CREDIT","EXCLU")
df['JournalLib'] = df["JournalLib"].str.replace("RELARING TO","RELATIF À")
df['JournalLib'] = df["JournalLib"].str.replace("CLEAN UP-","APUREMENT-")
df['JournalLib'] = df["JournalLib"].str.replace("2ND INSTALLEMENT","2ème versement")
df['JournalLib'] = df["JournalLib"].str.replace("DOUBLE PAYMENT","DOUBLE PAIEMENT")
df['JournalLib'] = df["JournalLib"].str.replace("CLEAN UP-","APUREMENT-")
df['JournalLib'] = df["JournalLib"].str.replace("DUTIES","DROITS")
df['JournalLib'] = df["JournalLib"].str.replace("Previous balance","Solde Précédent")
df['JournalLib'] = df["JournalLib"].str.replace("Cash fx","Cash FX")
df['JournalLib'] = df["JournalLib"].str.replace("PAYROLL INCOME","REVENU DE PAIE")
df['JournalLib'] = df["JournalLib"].str.replace("TELEPHONE CHARGES","Frais de Téléphone")
df['JournalLib'] = df["JournalLib"].str.replace("Clearing","Compensation")
df['JournalLib'] = df["JournalLib"].str.replace("Hotel","Hôtel")
df['JournalLib'] = df["JournalLib"].str.replace("Miscellaneous","Divers")
df['JournalLib'] = df["JournalLib"].str.replace("Corporate Card-Out-of-Poc","")
df['JournalLib'] = df["JournalLib"].str.replace("Traveling Dolby Empl","Employé itinérant de Dolby")
df['JournalLib'] = df["JournalLib"].str.replace("Tools-Equipment-Lab Supplies","Outils-Equipement-Fournitures de laboratoire")
df['JournalLib'] = df["JournalLib"].str.replace("rounding","Arrondissement")
df['JournalLib'] = df["JournalLib"].str.replace("Building Supplies-Maintenance","Matériaux de construction-Entretien")
df['JournalLib'] = df["JournalLib"].str.replace("Expensed Furniture","Mobilier Dépensé")
df['JournalLib'] = df["JournalLib"].str.replace("Credit for Charges","Crédit pour frais")
df['JournalLib'] = df["JournalLib"].str.replace("Manual P-ment and double payment to be deduct","P-mnt manuel et double paiement à déduire")
df['JournalLib'] = df["JournalLib"].str.replace("Employee insurance travel","Assurance de voyage des employés 2019")
df['JournalLib'] = df["JournalLib"].str.replace("Rent ","Location ")
df['JournalLib'] = df["JournalLib"].str.replace("Lunch vouchers ","Bons déjeuner")
df['JournalLib'] = df["JournalLib"].str.replace("Store Room ","Chambre Stocke")
df['JournalLib'] = df["JournalLib"].str.replace("Evaluation ","Évaluation  ")
df['JournalLib'] = df["JournalLib"].str.replace("Charges ","Frais ")
df['JournalLib'] = df["JournalLib"].str.replace("On Line ","En ligne ")
df['JournalLib'] = df["JournalLib"].str.replace("/Building Supplies/Maintenance","/ Matériaux de construction / Entretien")
df['JournalLib'] = df["JournalLib"].str.replace("Music Instruments","Instruments Musicales")
df['JournalLib'] = df["JournalLib"].str.replace("/Employee Awards/Recognition", "/ Récompenses des employés / Reconnaissance")


df['JournalLib'] = df["JournalLib"].str.replace("/Daily Allowance","/Indemnité journalière")

df['JournalLib'] = df["JournalLib"].str.replace("RECLASS ", "RECLASSIFICATION ")
df['JournalLib'] = df["JournalLib"].str.replace("Purchase Accounting", "Comptabilité d'achat")
df['JournalLib'] = df["JournalLib"].str.replace( "EXPAT ", " Expatrié ")
df['JournalLib'] = df["JournalLib"].str.replace("FROM ", "DE ")
df['JournalLib'] = df["JournalLib"].str.replace("INVOICE", "FACTURE")
df['JournalLib'] = df["JournalLib"].str.replace("CLEANUP", "APUREMENT")
df['JournalLib'] = df["JournalLib"].str.replace("Repayment", "Restitution")

df['JournalLib'] = df["JournalLib"].str.replace("Office Furniture", "Meubles de bureau")
df['JournalLib'] = df["JournalLib"].str.replace("anti-stress treatments", "traitements anti-stress")

df['JournalLib'] = df["JournalLib"].str.replace("UK Tax Return", "Décl. d'impôt Royaume-Uni")
df['JournalLib'] = df["JournalLib"].str.replace("Office Location", "Location de bureau")
df['JournalLib'] = df["JournalLib"].str.replace("Deliver Service", "Service de livraison")
df['JournalLib'] = df["JournalLib"].str.replace("Foreign Office Support", "Soutien aux bureaux étrangères")
df['JournalLib'] = df["JournalLib"].str.replace("Showroom", "Salle d'exposition")

df['JournalLib'] = df["JournalLib"].str.replace("aditional Services", "Services supplémentaires ")
df['JournalLib'] = df["JournalLib"].str.replace("Cofee consumption Paris office", "Consommation de café Bureau de Paris")

df['JournalLib'] = df["JournalLib"].str.replace("Consultant ", "Expert-conseil")
df['JournalLib'] = df["JournalLib"].str.replace("INVOICE", "FACTURE")
df['JournalLib'] = df["JournalLib"].str.replace("Rent-", "Location-")
df['JournalLib'] = df["JournalLib"].str.replace("Corporate", "Entreprise")
df['JournalLib'] = df["JournalLib"].str.replace("COST ", "COÛT ")
df['JournalLib'] = df["JournalLib"].str.replace("TRAINING", "Formation")
df['JournalLib'] = df["JournalLib"].str.replace("LIFE DISAB", "Invalidité")
df['JournalLib'] = df["JournalLib"].str.replace("INSU ", "ASSURANCE ")
df['JournalLib'] = df["JournalLib"].str.replace("PATENT AWARD", "BREVET")

df['JournalLib'] = df["JournalLib"].str.replace("EQUIVALENT POUR UNUSED VACATION POUR LEAVE", "CONGÉ DE VACANCES INUTILISÉS")
df['JournalLib'] = df["JournalLib"].str.replace("SPOT ", "")
df['JournalLib'] = df["JournalLib"].str.replace("AIRFARE TRANSFER TO PREPAIDS", "TRANSFERT DE TRANSPORT AÉRIEN À PAYÉ D'AVANCE")
df['JournalLib'] = df["JournalLib"].str.replace("WITHHOLDING", "RETRAIT")
df['JournalLib'] = df["JournalLib"].str.replace("Clear ", "Reglement ")
df['JournalLib'] = df["JournalLib"].str.replace("Clear ", "Reglement ")
df['JournalLib'] = df["JournalLib"].str.replace("Rent/", "Location/")
df['JournalLib'] = df["JournalLib"].str.replace("Pay ", "Paiement ")
df['JournalLib'] = df["JournalLib"].str.replace("PAYMENT", "Paiement ")

df['JournalLib'] = df["JournalLib"].str.replace("French Income Tax Return;", "Déclaration de revenus française;")
df['JournalLib'] = df["JournalLib"].str.replace("REVESERVICES", "SERVICES")
df['JournalLib'] = df["JournalLib"].str.replace("INCLUDED DOUBLE", "DOUBLE INCLUS")
df['JournalLib'] = df["JournalLib"].str.replace("Bank", "Banque")
df['JournalLib'] = df["JournalLib"].str.replace("/Promotional Expenses", "/Frais de promotion")

df['JournalLib'] = df["JournalLib"].str.replace(" ACTIVITY ", " activité ")
df['JournalLib'] = df["JournalLib"].str.replace(" DEFINED BENEFIT LIABILITY", "PASSIF À AVANTAGES DÉTERMINÉES")
df['JournalLib'] = df["JournalLib"].str.replace("COÛT PLUS ", "Revient Majoré")
df['JournalLib'] = df["JournalLib"].str.replace("/Airline Frais", "/Tarifs aériens")
df['JournalLib'] = df["JournalLib"].str.replace("/Tools/Equipment/Lab Supplies", "/Outils / Équipement / Fournitures de laboratoire")
df['JournalLib'] = df["JournalLib"].str.replace("Rent/", "Location/")
df['JournalLib'] = df["JournalLib"].str.replace("Payment Posting", "Paiements")
df['JournalLib'] = df["JournalLib"].str.replace("COMMISSION D’ACCUMULATION", "ACCUMULATIONS DE COMISSIONS")
df['JournalLib'] = df["JournalLib"].str.replace("ImpôtE", "Impôt")
df['JournalLib'] = df["JournalLib"].str.replace("MED.INSU", "MED.ASSURANCE")
df['JournalLib'] = df["JournalLib"].str.replace("APPRENTICESHIP_CONTRIBUTIONS_TRUE_UP", "CONTRIBUTIONS À L'APPRENTISSAGE/TRUE UP")
df['JournalLib'] = df["JournalLib"].str.replace("NET PAY", "SALAIRE NET")
df['JournalLib'] = df["JournalLib"].str.replace("CASH ", "ARGENT ")
df['JournalLib'] = df["JournalLib"].str.replace("Repayment ", "Repaiement ")
df['JournalLib'] = df["JournalLib"].str.replace("Acct. ", "Comptab. ")

df['JournalLib'] = df["JournalLib"].str.replace("ACCR ", "ACC ")
df['JournalLib'] = df["JournalLib"].str.replace("Accr ", "Acc.")
df['JournalLib'] = df["JournalLib"].str.replace("Cash Balance", "Solde de caisse")
df['JournalLib'] = df["JournalLib"].str.replace("RECLASS ", "RECLASSEMENT ")
df['JournalLib'] = df["JournalLib"].str.replace("VAT FILING ", "Dépôt de TVA ")
df['JournalLib'] = df["JournalLib"].str.replace("Needs to be re-booked due", "KI")
df['JournalLib'] = df["JournalLib"].str.replace("reclass from", "reclasser de")
df['JournalLib'] = df["JournalLib"].str.replace("RECLASS FROM", "reclasser de")
df['JournalLib'] = df["JournalLib"].str.replace("PAYROLL", "PAIE")
df['JournalLib'] = df["JournalLib"].str.replace("RECLASS ", "Reclasser")

df['JournalLib'] = df["JournalLib"].str.replace("DEDICTION","DEDUCTION")
df['JournalLib'] = df["JournalLib"].str.replace("Cash","Argent ")
df['JournalLib'] = df["JournalLib"].str.replace("cash ","argent ")
df['JournalLib'] = df["JournalLib"].str.replace("ReclasserIFICATIO","RECLASSEMENT ")
df['JournalLib'] = df["JournalLib"].str.replace("ImpôtS ","Impôts ")
df['JournalLib'] = df["JournalLib"].str.replace("Working Repas (Employees Only) ","Repas de travail (employés seulement) ")
df['JournalLib'] = df["JournalLib"].str.replace("/Banque Frais","/Frais Bancaires")
df['JournalLib'] = df["JournalLib"].str.replace("MED. INS.","ASSURANCE MED.")
df['JournalLib'] = df["JournalLib"].str.replace("AJE WIRE LOG TRAN","AJE VERSEMENT")
df['JournalLib'] = df["JournalLib"].str.replace("JUN'","JUIN'")
df['JournalLib'] = df["JournalLib"].str.replace("Deferred Rent18 rue de Lo'","Loyer différé 18 Rue de Lo'")

print("Doc Headers successfully translated! Please note the new columns will be called JournalLib and will be at the end of the excel sheet")
print("The next cell is going to map the account numbers to french numbers and names according to the file mapping-accounts.xlsx also available in box")

## MAPPING OF ACCOUNTS 

accounts = pd.read_excel("mapping-accounts.xlsx")
accounts1 = accounts[['G/L Account #','FrAcc']] 
accounts2 = accounts[['G/L Account #','FrName']]
df['CompteNum'] = df[e].copy()
df['CompteLib'] = df[e].copy()
accounts1 = accounts1.set_index('G/L Account #').to_dict()['FrAcc']
accounts2 = accounts2.set_index('G/L Account #').to_dict()['FrName']
df['CompteLib'] = df['CompteLib'].replace(accounts2)
df['CompteNum'] = df['CompteNum'].map(accounts1).astype(str) + df['CompteNum'].astype(str) 

df['CompteNum'] = df["CompteNum"].str.replace('.0','')

print("Your accounts were successfully matched! The accounts are going to be in this format: 123.0456.05")
print("because python reads them as numbers. In excel, you can use the replace function to replace .0 to nothing, and your accounts should be in the correct format then")
print("Please note the new columns will be called CompteLib and CompteNum and will be at the end of the excel sheet")

## saving your new file to a excel format. The last cells should be the new ones if your cell names
## were different than the FEC standard, if not they are going to replace your old cells. In this cas
## make save your new file under a different name 

file_name = input("Name of the new file with .xlsx:")

writer = pd.ExcelWriter(file_name,
                        engine='xlsxwriter',
                        datetime_format='yyyymmdd',
                        date_format='yyyymmdd')

df.to_excel(writer, sheet_name = ('Sheet1'))

workbook  = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_column('B:C', 20)
writer.save()


print("Your file was successfully save under the name", file_name)
print("The new file should be in the downloads folder!")
