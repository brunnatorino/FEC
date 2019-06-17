import pandas as pd 

df = pd.read_excel("FEC2.xlsx")

print(df['EcritureLib'].head())

df['EcritureLib'] = df["EcritureLib"].str.replace('VAT', 'TVA')
df['EcritureLib'] = df["EcritureLib"].str.replace('SEPTEMBER', 'SEPT')
df['EcritureLib'] = df["EcritureLib"].str.replace('TAXBACK', 'Reboursement')
df['EcritureLib'] = df["EcritureLib"].str.replace('REPORT', '')
df['EcritureLib'] = df["EcritureLib"].str.replace("Reverse Posting", "Contre Passationd'Ecriture")
df['EcritureLib'] = df["EcritureLib"].str.replace("BASE RENT", "Location Base")
df['EcritureLib'] = df["EcritureLib"].str.replace("Rent", "Location")
df['EcritureLib'] = df["EcritureLib"].str.replace("RENT", "Location")
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
df['EcritureLib'] = df["EcritureLib"].str.replace("COST-PLUS SERVICE REVENUE", "REVENUS DE SERVICE COÛT-PLUS")
df['EcritureLib'] = df["EcritureLib"].str.replace("SETTLEMENT", "RÈGLEMENT ")
df['EcritureLib'] = df["EcritureLib"].str.replace("PURCHASE", "ACHAT")
df['EcritureLib'] = df["EcritureLib"].str.replace("NON-CP SETTLE", "RÈGLEMENT NON-CP")
df['EcritureLib'] = df["EcritureLib"].str.replace("PAID", "Payé")
df['EcritureLib'] = df["EcritureLib"].str.replace("FEES", "Frais")

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

df['EcritureLib'] = df["EcritureLib"].str.replace("Feb.", "Fév.")
df['EcritureLib'] = df["EcritureLib"].str.replace("Mar.", "Mars")
df['EcritureLib'] = df["EcritureLib"].str.replace("Apr.", "Avril")
df['EcritureLib'] = df["EcritureLib"].str.replace("Aug.", "Août")

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
df['EcritureLib'] = df["EcritureLib"].str.replace("Office","Bureau")
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


df['EcritureLib'] = df["EcritureLib"].str.replace("Annual Electrical Verification", "Vérification électrique annuelle ")
df['EcritureLib'] = df["EcritureLib"].str.replace("Health costs ", "Coûts santé")
df['EcritureLib'] = df["EcritureLib"].str.replace("Unlimited-receipt and policy audit", "Vérification illimitée des reçus et audites")
df['EcritureLib'] = df["EcritureLib"].str.replace("Water fountain ", "Fontaine d'eau")
df['EcritureLib'] = df["EcritureLib"].str.replace("Quartely control visit", "Visite de contrôle trimestrielle")
df['EcritureLib'] = df["EcritureLib"].str.replace("Fire extinguishers annual check", "Vérification annuelle des extincteurs")
df['EcritureLib'] = df["EcritureLib"].str.replace("showroom rent", "location de salle d'exposition")





mapping_Valuation = {" Valuation on": " Évaluation sur"," Valuation on Reverse":" Évaluation sur Contre Passation",
                     " Reverse Posting":" Contre Passation d'Ecriture -  Conversion de devise sur",
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
              "TRAINING TAX TRUE UP":"TAXE DE FORMATION"}

df['EcritureLib'] = df["EcritureLib"].str.replace("/", "-")


df1 = df.replace({"EcritureLib":mapping_Valuation}, regex=True)
df1 = df1.replace({"EcritureLib":mapping_AA}, regex=True)


df1['EcritureLib'].to_excel("test2.xlsx")
