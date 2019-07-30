import pandas as pd
from gooey import Gooey, GooeyParser
import numpy as np
import xlsxwriter
import xlrd

@Gooey(program_name="FEC")
def parse_args():
    parser = GooeyParser()

    parser.add_argument('data_file',
                        action='store',
                        widget='FileChooser',
                        help="Excel file from SAP G/L View")

    parser.add_argument('parked_and_noted',
                        action='store',
                        widget='FileChooser',
                        help="Only Parked and Noted Items")
    
    parser.add_argument('deleted_items',
                        action='store',
                        widget='FileChooser',
                        help="Only Deleted Items")

    args = parser.parse_args()
    return args

def combine(file, file2, file3):
    gl_df = pd.read_excel(file)
    parked_df = pd.read_excel(file2)
    delete_df = pd.read_excel(file3)
    
    numbers = gl_df['Document Number'].tolist()

    gl = gl_df.append(parked_df[~parked_df['Document Number'].isin(numbers)])
    gl = gl.append(delete_df[~delete_df['Document Number'].isin(numbers)])

    gl = gl.reset_index()
    
    return gl


def transform(gl):
    
    gl['JournalCode'] = gl['Document Type']
    gl['JournalLib'] = gl['Document Header Text']
    gl['EcritureNum'] = gl['Document Number']
    gl['EcritureDate'] = gl['Posting Date']
    gl['CompteNum'] = gl['G/L Account']
    gl['CompteLib'] = gl['G/L Account']
    gl['CompAuxLib'] = gl['Offsetting acct no.']
    gl['PieceRef'] = gl['Reference']
    gl['EcritureLib'] = gl['Text']
    gl['Amount'] = gl['Amount in local currency']
    gl['MontantDevise'] = gl['Amount in loc.curr.2']
    gl['Idevise'] = 'USD'
    gl['PieceDate'] = gl['Document Date']
    gl['ValidDate'] = gl['Entry Date']
    gl['EcritureLet'] = gl['Assignment']
    gl['DateLet'] = gl['Entry Date']

    gl.loc[gl["Amount"] < 0 ,'Credit'] = gl['Amount']
    gl.loc[gl["Amount"] > 0 ,'Debit'] = gl['Amount']

    gl.loc[gl["Debit"].isnull() ,'Debit'] = 0
    gl.loc[gl["Credit"].isnull() ,'Credit'] = 0

    gl.loc[gl["EcritureLet"].isnull(),'DateLet'] = ''
    gl.loc[gl["EcritureLet"].isnull(),'DateLet'] = ''

    gl.loc[(gl.Debit == 0) & (gl.Credit == 0),'MontantDevise'] = gl['MontantDevise']
    gl.loc[(gl.Debit != 0) | (gl.Credit != 0),'MontantDevise'] = ''
    gl.loc[gl["MontantDevise"] == '','Idevise'] = ''

    accounts = pd.read_excel("mapping-accounts.xlsx")
    accounts1 = accounts[['G/L Account #','FrMap']] 
    accounts2 = accounts[['G/L Account #','FEC Compliant']]

    accounts1 = accounts1.set_index('G/L Account #').to_dict()['FrMap']
    accounts2 = accounts2.set_index('G/L Account #').to_dict()['FEC Compliant']
    gl['CompteLib'] = gl['CompteLib'].replace(accounts2)
    gl['CompteNum'] = gl['CompteNum'].map(accounts1).astype(str) + gl['CompteNum'].astype(str)
    journals = pd.read_excel("test128.xlsx")
    codes = pd.read_excel('mapping-journal.xlsx')
    journals = journals.set_index('DocHeader').to_dict()['JournalLib_FR']
    codes = codes.set_index('JournalCode').to_dict()["JournalLib_FR"]

    gl.loc[gl["JournalLib"].isnull(),'JournalLib'] = gl["JournalCode"].map(str)
    gl['JournalLib'] = gl['JournalLib'].replace(journals)
    gl['JournalLib'] = gl['JournalLib'].replace(codes)
    vendors = pd.read_excel("Vendors1.xlsx")
    vendors = vendors.set_index('No').to_dict()['Name']
    gl['CompAuxLib'] = gl['CompAuxLib'].map(vendors)
    gl['CompAuxNum'] = "F" + gl['CompAuxLib']
    gl.loc[(~gl.CompAuxLib.isnull()) & (gl["EcritureLib"].isnull()),'EcritureLib'] = gl['JournalLib'].map(str) + " de " + gl['CompAuxLib'].map(str)
    gl.loc[(gl.CompAuxLib.isnull()) & (gl["EcritureLib"].isnull()),'EcritureLib'] = gl['JournalLib'].map(str) + gl['EcritureNum'].map(str)

    gl['EcritureLib'] = gl['EcritureLib'].str.replace('^\d+', '')

    mapping_Valuation = {" Valuation on": " Ã‰valuation sur"," Valuation on Reverse":" Ã‰valuation sur Contre Passation",
                         " Reverse Posting":" Contre-Passation d'Ecriture -  Conversion de devise sur",
                         " Translation Using":" Conversion de devise sur"}
    mapping_AA = {"Reclass from": " Reclassification de", "reclass from": " Reclassification de", "ZEE MEDIA":"ZEE MEDIA Campaignes NumÃ©riques", "TRAINING CONTRI. ER JANUARY '19":"FORMATION CONTRI. ER JANVIER' 19",
                  "TAX FEES":"Taxes","SOCIAL SECURITY: URSSAF":"SÃ‰CURITÃ‰ SOCIALE: URSSAF","SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTIONS Ã€ LA FORMATION",
                  "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTION Ã€ Lâ€™APPRENTISSAGE","RSM":"SERVICES DE PAIE RSM EF18","RSA":"SERVICES DE PAIE RSA OCT-JAN",
                  "PRIVATE HEALTH":"SANTÃ‰ PRIVÃ‰E: ASSURANCE MÃ‰DICALE-AXA/","PENSION: PENSION CONTRIBUTIONS - REUNICA":"PENSION: COTISATIONS DE RETRAITE-REUNICA","PENSION: LIFE & DISABILITY INSURANCE - R":"PENSION: ASSURANCE VIE & INVALIDITÃ‰-R", 
                  "PENSION JANUARY '19":"PENSION JANVIER '19",
                  "ON CALL JANUARY '19":"Disponible Janvier'19",
                  "NRE + PROJECT INITIATION FEES":"NRE + FRAIS Dâ€™INITIATION AU PROJET (PO 750003","NET PAY JANUARY '19":"Payeante Janvier'19","JANUARY'19":"JANVIER'19",
                  "LUNCH VOUCHER- WITHHOLDING":"BON DÃ‰JEUNER-RETENUE","HOLIDAY BONUS ACCRUAL FY18/19":"CUMUL DES PRIMES DE VACANCES EF18/19",
                  "GROSS SALARY JANUARY '19":"SALAIRE BRUT JANVIER' 19","EMEA ACCRUAL P8FY19":"P8FY19 Dâ€™ACCUMULATION EMEA","COMMISSION RE-ACCRUAL":"COMMISSION RÃ‰-ACCUMULATION",
                  "COMMISSION ACCRUAL":"COMMISSION Dâ€™ACCUMULATION","MARCH":"MARS","MAY":"MAI","APRIL":"AVRIL","AUDIT FEES":"HONORAIRES Dâ€™AUDIT",
                  "UNSUBMITTED_UNPOSTED BOA ACCRUAL":"Accumulation BOA non soumise non exposÃ©e","UNASSIGNED CREDITCARD BOA ACCRUAL":"NON ASSIGNÃ‰ CREDITCARD BOA ACCUMULATION ",
                  "EMEA ACCRUAL":"ACCUMULATION EMEA","Exhibit Expenses":"Frais d'exposition","Hotel Tax":"Taxe hÃ´teliÃ¨re","Company Events":"Ã‰vÃ©nements d'entreprise",
                  "Public Transport":"Transport public", "Agency Booking Fees":"Frais de rÃ©servation d'agence","Working Meals (Employees Only)":"Repas de travail (employÃ©s seulement)",
                  "Airfare":"Billet d'avion","Office Supplies":"Fournitures de bureau","Tolls":"PÃ©ages",
                  "write off difference see e-mail attached":"radiation de la diffÃ©rence voir e-mail ci-joint",
                 "Manual P/ment and double payment to be deduct":"P/ment manuel et double paiement Ã  dÃ©duire","FX DIFFERENCE ON RSU":"DIFFERENCE FX SUR RSU",
                 "DEFINED BENEFIT LIABILITY-TRUE UP":"RESPONSABILITÃ‰ Ã€ PRESTATIONS DÃ‰TERMINÃ‰ES-TRUE UP","EXTRA RELEASE FOR STORAGE REVERSED":"EXTRA LIBERATION POUR STOCKAGE CONTREPASSATION",
                 "RECLASS BANK CHARGES TO CORRECT COST CEN":"RECLASSER LES FRAIS BANCAIRES POUR CORRIGER","PAYROLL INCOME TAXES":"IMPÃ”TS SUR LES SALAIRES",
                  "TRAINING TAX TRUE UP":"TAXE DE FORMATION", "FX DIFFERENCE ON STOCK OPTION EXERCISES":"FX DIFFERENCE SUR LES EXERCICES D'OPTIONS STOCK",
                  "Airline Frais":"Frais de Transport AÃ©rien","Agency Booking Fees":"Frais de RÃ©servation d'Agence","Computer Supplies":"Fournitures informatiques",
                 "AUDIT FEES":"FRAIS D'AUDIT", "HOLIDAY BONUS ACCRUAL ":"ACCUMULATION DE BONUS DE VACANCES","TAX FEES":"FRAIS D'IMPÃ”T",
                  "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUITION Ã€ Lâ€™APPRENTISSAGE",
                  "SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTIONS Ã€ LA FORMATION", "TRAVEL COST":"FRAIS DE VOYAGE", "HOUSING TAX":"TAXE SUR LE LOGEMENT", 
                 "PAYROLL INCOME TAXES":"IMPÃ”TS SUR LE REVENU DE LA PAIE","INCOME TAX-PAS":"IMPÃ”T SUR LE REVENU-PAS", "IC SETTLEMENT":"RÃ¨glement Interentreprises",
                 "VACATION TAKEN":"VACANCES PRISES", "SOCIAL SECURITY: APPR. CONTR.":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTION Ã€ Lâ€™APPRENTISSAGE", 
                  "POST OF AVRIL DEC IN CORRECT SIGN":"CORRECTION D'ECRITURE AVRIL DEC"}



    gl = gl.replace({"EcritureLib":mapping_Valuation}, regex=True)
    gl = gl.replace({"EcritureLib":mapping_AA}, regex=True)

    gl['EcritureLib'] = gl["EcritureLib"].str.replace('COST-PLUS', 'Revient MajorÃ©')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('PRITVAE HEALTH: MEDICAL INSURANCE', 'SANTÃ‰ PRIVÃ‰E: ASSURANCE MÃ‰DICALE')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('MEDICAL INSURANCE', 'ASSURANCE MÃ‰DICALE')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('UNASSIGNED', 'NON ATTRIBUÃ‰')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('Payout', 'Paiement')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('FRINGE COST', 'COÃ›T MARGINAL')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('PROJECT INITIATION', 'LANCEMENT DU PROJET')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('ACCRUAL', 'ACCUMULATION')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('CREDITCARD', 'CARTE DE CRÃ‰DIT')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('ACCR ', 'ACCUM ')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('VAT ', 'TVA ')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('SOCIAL SECURITY ', 'SÃ‰CURITÃ‰ SOCIALE')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('SEPTEMBER', 'SEPT')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('TAXBACK', 'Reboursement')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('REPORT', '')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Reverse Posting", "Contre Passation d'Ecriture")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("BASE RENT", "Location Base")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Rent ", "Location ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RENT ", "Location ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CLEARING", "compensation ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("clearing", "compensation ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("BILLING CHARGES", "FRAIS DE FACTURATION ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("UNPAID", "NON PAYÃ‰")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PROPERTY TAX", "IMPÃ”T FONCIER ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Trans. Using", "Conversion sur")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("SALARIES", "Salaires")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Refund", "Remboursement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("REFUND", "Remboursement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("no invoice", "pas de facture")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("COST-PLUS SERVICE REVENUE", "Revenus de service Revient MajorÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("SETTLEMENT", "RÃˆGLEMENT ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PURCHASE", "ACHAT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("NON-CP SETTLE", "RÃˆGLEMENT NON-CP")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PAID ", " PayÃ© ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FEES ", "Frais")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("January", "Janvier")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("February", "FÃ©vrier")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("March", "Mars")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("April", "Avril")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("May", "Mai")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("June", "Juin")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("July", "Juillet")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("September", "Septembre")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Aug.", "AoÃ»t")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("JANUARY", "Janvier")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FEBRUARY", "FÃ©vrier")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("MARCH", "Mars")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("APRIL", "Avril")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("MAY", "Mai")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("JUNE", "Juin")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("JULY", "Juillet")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("SEPTEMBER", "Septembre")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("AUGUST.", "AoÃ»t")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("NOVEMBER.", "Novembre")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("DECEMBER.", "DÃ©cembre")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("December", "DÃ©cembre")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Feb.", "FÃ©v.")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Mar.", "Mars")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Apr.", "Avril")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Aug.", "AoÃ»t")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Aug.", "AoÃ»t")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Reverse ", "Contre-passation ")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INTEREST CHARGE", "CHARGE D'INTÃ‰RÃŠT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("-SICK LEAVE PAY", "-Paiement congÃ© maladie")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RECLASSEMENTIFICATION", "RECLASSIFICATION")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INSTALMENT", "VERSEMENT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FIRST", "1ere")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FINE LATE PAY.", "Amende pour retard de paiement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("-PATERNITY PAY", "IndemnitÃ©s de paternitÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("SOCIAL SECURITY:", "SÃ‰CURITÃ‰ SOCIALE:")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Trip from", "Voyage de:")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace(" To ", " Ã ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Shipping", "Livraison")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("VOXEET INTEGRATION COSTS", "COÃ›TS D'INTÃ‰GRATION DE VOXEET")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INCOME TAX", "IMPÃ”T SUR LE REVENU")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('Rideshare', 'Covoiturage')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('Travel Meals', 'Repas de Travail')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('Fees', 'Frais')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace('Phone', 'TÃ©lÃ©phone')
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Books", "Abonnements")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Subcriptions", "Location Base")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Meals", "Repas")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Entertainment", "divertissement ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Third Party", "tiers ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Training Fees", "Frais d0 Formation")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Conferences/Tradeshows Registratio", "ConfÃ©rences/Tradeshows Enregistrement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FOR", "POUR")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ROUNDING", "ARRONDISSEMENT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("STORAGE", "STOCKAGE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("VACATION ACCURAL", "Vacances AccumulÃ©es")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RECEIVABLE ", "Recevables")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("AFTER PAYOUT ", "APRÃˆS PAIEMENT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CLEAN UP ", "APUREMENT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("EMPLOYEE TRAVEL INSUR ", "ASSURANCE DE VOYAGE DES EMPLOYÃ‰S")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CORRECTION OF", "CORRECTION DE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("TAXES PAYROLL", "IMPÃ”TS SUR LA MASSE SALARIALE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ACCOUNT", "COMPTE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("TAX", "ImpÃ´t")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("life disab", "IncapacitÃ© de vie")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("HOUSING TAX","TAXE D'HABITATION")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("GROSS SALARY","SALAIRE BRUT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Cleaning Services","Nettoyage")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Freight","Fret")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Membership","adhÃ©sion")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Air cooling Maintenance","Entretien de refroidissement de l'air")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Power on Demand Platform","Plateforme d'energie Ã  la demande")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Sanitaire room installation"," Installation de la salle sanitaire")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("subscription","abonnement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Coffee supplies "," Fournitures de cafÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Duty and Tax ","Devoir et fiscalitÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Electricity ","ElectricitÃ© ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Lunch vouchers  ","Bons dÃ©jeuner")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Security monitoring","Surveillance de la sÃ©curitÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Water", "L'EAU")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Statutory Audit", "Audit statutaire")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace(" Meeting room screen installation", "Installation de l'Ã©cran de la salle de rÃ©union")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Water", "L'EAU")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Water", "L'EAU")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Tax Credit FY 2016", "CrÃ©dit d'impÃ´t Exercice 2016")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Bank of America Merill Lynch-T&E statement","DÃ©claration de Merill Lynch")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("English Translation", "Traduction anglaise")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Office Rent", "Location de Bureau")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Annual Electrical Verification", "VÃ©rification Ã©lectrique annuelle ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Health costs ", "CoÃ»ts santÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Unlimited-receipt and policy audit", "VÃ©rification illimitÃ©e des reÃ§us et audites")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Water fountain ", "Fontaine d'eau")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Quartely control visit", "Visite de contrÃ´le trimestrielle")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Fire extinguishers annual check", "VÃ©rification annuelle des extincteurs")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("showroom rent", "location de salle d'exposition")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("AND ACTUAL RECEIV","ET RECETTES RÃ‰ELLES")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FILING","DÃ‰PÃ”T")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ORDERS","ORDRES")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("EXCLUDED -DUMMY CREDIT","EXCLU")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RELARING TO","RELATIF Ã€")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CLEAN UP-","APUREMENT-")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("2ND INSTALLEMENT","2Ã¨me versement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("DOUBLE PAYMENT","DOUBLE PAIEMENT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CLEAN UP-","APUREMENT-")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("DUTIES","DROITS")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Previous balance","Solde PrÃ©cÃ©dent")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Cash fx","Cash FX")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PAYROLL INCOME","REVENU DE PAIE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("TELEPHONE CHARGES","Frais de TÃ©lÃ©phone")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Clearing","Compensation")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Hotel","HÃ´tel")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Miscellaneous","Divers")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Corporate Card-Out-of-Poc","")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Traveling Dolby Empl","EmployÃ© itinÃ©rant de Dolby")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Tools-Equipment-Lab Supplies","Outils-Equipement-Fournitures de laboratoire")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("rounding","Arrondissement")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Building Supplies-Maintenance","MatÃ©riaux de construction-Entretien")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Expensed Furniture","Mobilier DÃ©pensÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Credit for Charges","CrÃ©dit pour frais")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Manual P-ment and double payment to be deduct","P-mnt manuel et double paiement Ã  dÃ©duire")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Employee insurance travel","Assurance de voyage des employÃ©s 2019")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Rent ","Location ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Lunch vouchers ","Bons dÃ©jeuner")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Store Room ","Chambre Stocke")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Evaluation ","Ã‰valuation  ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Charges ","Frais ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("On Line ","En ligne ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Building Supplies/Maintenance","/ MatÃ©riaux de construction / Entretien")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Music Instruments","Instruments Musicales")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Employee Awards/Recognition", "/ RÃ©compenses des employÃ©s / Reconnaissance")


    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Daily Allowance","/IndemnitÃ© journaliÃ¨re")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RECLASS ", "RECLASSIFICATION ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Purchase Accounting", "ComptabilitÃ© d'achat")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace( "EXPAT ", " ExpatriÃ© ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("FROM ", "DE ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INVOICE", "FACTURE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CLEANUP", "APUREMENT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Repayment", "Restitution")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Office Furniture", "Meubles de bureau")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("anti-stress treatments", "traitements anti-stress")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("UK Tax Return", "DÃ©cl. d'impÃ´t Royaume-Uni")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Office Location", "Location de bureau")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Deliver Service", "Service de livraison")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Foreign Office Support", "Soutien aux bureaux Ã©trangÃ¨res")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Showroom", "Salle d'exposition")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("aditional Services", "Services supplÃ©mentaires ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Cofee consumption Paris office", "Consommation de cafÃ© Bureau de Paris")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Consultant ", "Expert-conseil")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INVOICE", "FACTURE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Rent-", "Location-")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Corporate", "Entreprise")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("COST ", "COÃ›T ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("TRAINING", "Formation")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("LIFE DISAB", "InvaliditÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INSU ", "ASSURANCE ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PATENT AWARD", "BREVET")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("EQUIVALENT POUR UNUSED VACATION POUR LEAVE", "CONGÃ‰ DE VACANCES INUTILISÃ‰S")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("SPOT ", "")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("AIRFARE TRANSFER TO PREPAIDS", "TRANSFERT DE TRANSPORT AÃ‰RIEN Ã€ PAYÃ‰ D'AVANCE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("WITHHOLDING", "RETRAIT")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Clear ", "Reglement ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Clear ", "Reglement ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Rent/", "Location/")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Pay ", "Paiement ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PAYMENT", "Paiement ")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("French Income Tax Return;", "DÃ©claration de revenus franÃ§aise;")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("REVESERVICES", "SERVICES")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("INCLUDED DOUBLE", "DOUBLE INCLUS")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Bank", "Banque")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Promotional Expenses", "/Frais de promotion")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace(" ACTIVITY ", " activitÃ© ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace(" DEFINED BENEFIT LIABILITY", "PASSIF Ã€ AVANTAGES DÃ‰TERMINÃ‰ES")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("COÃ›T PLUS ", "Revient MajorÃ©")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Airline Frais", "/Tarifs aÃ©riens")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Tools/Equipment/Lab Supplies", "/Outils / Ã‰quipement / Fournitures de laboratoire")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Rent/", "Location/")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Payment Posting", "Paiements")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("COMMISSION Dâ€™ACCUMULATION", "ACCUMULATIONS DE COMISSIONS")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ImpÃ´tE", "ImpÃ´t")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("MED.INSU", "MED.ASSURANCE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("APPRENTICESHIP_CONTRIBUTIONS_TRUE_UP", "CONTRIBUTIONS Ã€ L'APPRENTISSAGE/TRUE UP")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("NET PAY", "SALAIRE NET")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("CASH ", "ARGENT ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Repayment ", "Repaiement ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Acct. ", "Comptab. ")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ACCR ", "ACC ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Accr ", "Acc.")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Cash Balance", "Solde de caisse")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RECLASS ", "RECLASSEMENT ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("VAT FILING ", "DÃ©pÃ´t de TVA ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Needs to be re-booked due", "KI")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("reclass from", "reclasser de")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RECLASS FROM", "reclasser de")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("PAYROLL", "PAIE")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("RECLASS ", "Reclasser")

    gl['EcritureLib'] = gl["EcritureLib"].str.replace("DEDICTION","DEDUCTION")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Cash","Argent ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("cash ","argent ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ReclasserIFICATIO","RECLASSEMENT ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("ImpÃ´tS ","ImpÃ´ts ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Working Repas (Employees Only) ","Repas de travail (employÃ©s seulement) ")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("/Banque Frais","/Frais Bancaires")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("MED. INS.","ASSURANCE MED.")
    gl['EcritureLib'] = gl["EcritureLib"].str.replace("Facture - Brut'","Facture - Brute'")


    gl['EcritureLib'] = gl['EcritureLib'].str.replace('-', '')
    gl['EcritureLib'] = gl['EcritureLib'].str.replace('/', '')
    gl['EcritureLib'] = gl['EcritureLib'].str.replace('Contre Passation', 'CP')

    mapping_Valuation1 = {" Valuation on": " Ã‰valuation sur"," Valuation on Reverse":" Ã‰valuation sur Contre Passation",
                         " Reverse Posting":" Contre-Passation d'Ecriture -  Conversion de devise sur",
                         " Translation Using":" Conversion de devise sur"}
    mapping_AA1 = {"Reclass from": " Reclassification de", "reclass from": " Reclassification de", "ZEE MEDIA":"ZEE MEDIA Campaignes NumÃ©riques", "TRAINING CONTRI. ER JANUARY '19":"FORMATION CONTRI. ER JANVIER' 19",
                  "TAX FEES":"Taxes","SOCIAL SECURITY: URSSAF":"SÃ‰CURITÃ‰ SOCIALE: URSSAF","SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTIONS Ã€ LA FORMATION",
                  "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTION Ã€ Lâ€™APPRENTISSAGE","RSM":"SERVICES DE PAIE RSM EF18","RSA":"SERVICES DE PAIE RSA OCT-JAN",
                  "PRIVATE HEALTH":"SANTÃ‰ PRIVÃ‰E: ASSURANCE MÃ‰DICALE-AXA/","PENSION: PENSION CONTRIBUTIONS - REUNICA":"PENSION: COTISATIONS DE RETRAITE-REUNICA","PENSION: LIFE & DISABILITY INSURANCE - R":"PENSION: ASSURANCE VIE & INVALIDITÃ‰-R", 
                  "PENSION JANUARY '19":"PENSION JANVIER '19",
                  "ON CALL JANUARY '19":"Disponible Janvier'19",
                  "NRE + PROJECT INITIATION FEES":"NRE + FRAIS Dâ€™INITIATION AU PROJET (PO 750003","NET PAY JANUARY '19":"Payeante Janvier'19","JANUARY'19":"JANVIER'19",
                  "LUNCH VOUCHER- WITHHOLDING":"BON DÃ‰JEUNER-RETENUE","HOLIDAY BONUS ACCRUAL FY18/19":"CUMUL DES PRIMES DE VACANCES EF18/19",
                  "GROSS SALARY JANUARY '19":"SALAIRE BRUT JANVIER' 19","EMEA ACCRUAL P8FY19":"P8FY19 Dâ€™ACCUMULATION EMEA","COMMISSION RE-ACCRUAL":"COMMISSION RÃ‰-ACCUMULATION",
                  "COMMISSION ACCRUAL":"COMMISSION Dâ€™ACCUMULATION","MARCH":"MARS","MAY":"MAI","APRIL":"AVRIL","AUDIT FEES":"HONORAIRES Dâ€™AUDIT",
                  "UNSUBMITTED_UNPOSTED BOA ACCRUAL":"Accumulation BOA non soumise non exposÃ©e","UNASSIGNED CREDITCARD BOA ACCRUAL":"NON ASSIGNÃ‰ CREDITCARD BOA ACCUMULATION ",
                  "EMEA ACCRUAL":"ACCUMULATION EMEA","Exhibit Expenses":"Frais d'exposition","Hotel Tax":"Taxe hÃ´teliÃ¨re","Company Events":"Ã‰vÃ©nements d'entreprise",
                  "Public Transport":"Transport public", "Agency Booking Fees":"Frais de rÃ©servation d'agence","Working Meals (Employees Only)":"Repas de travail (employÃ©s seulement)",
                  "Airfare":"Billet d'avion","Office Supplies":"Fournitures de bureau","Tolls":"PÃ©ages",
                  "write off difference see e-mail attached":"radiation de la diffÃ©rence voir e-mail ci-joint",
                 "Manual P/ment and double payment to be deduct":"P/ment manuel et double paiement Ã  dÃ©duire","FX DIFFERENCE ON RSU":"DIFFERENCE FX SUR RSU",
                 "DEFINED BENEFIT LIABILITY-TRUE UP":"RESPONSABILITÃ‰ Ã€ PRESTATIONS DÃ‰TERMINÃ‰ES-TRUE UP","EXTRA RELEASE FOR STORAGE REVERSED":"EXTRA LIBERATION POUR STOCKAGE CONTREPASSATION",
                 "RECLASS BANK CHARGES TO CORRECT COST CEN":"RECLASSER LES FRAIS BANCAIRES POUR CORRIGER","PAYROLL INCOME TAXES":"IMPÃ”TS SUR LES SALAIRES",
                  "TRAINING TAX TRUE UP":"TAXE DE FORMATION", "FX DIFFERENCE ON STOCK OPTION EXERCISES":"FX DIFFERENCE SUR LES EXERCICES D'OPTIONS STOCK",
                  "Airline Frais":"Frais de Transport AÃ©rien","Agency Booking Fees":"Frais de RÃ©servation d'Agence","Computer Supplies":"Fournitures informatiques",
                 "AUDIT FEES":"FRAIS D'AUDIT", "HOLIDAY BONUS ACCRUAL ":"ACCUMULATION DE BONUS DE VACANCES","TAX FEES":"FRAIS D'IMPÃ”T",
                  "SOCIAL SECURITY: APPRENTICESHIP CONTRIBU":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUITION Ã€ Lâ€™APPRENTISSAGE",
                  "SOCIAL SECURITY: TRAINING CONTRIBUTIONS":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTIONS Ã€ LA FORMATION", "TRAVEL COST":"FRAIS DE VOYAGE", "HOUSING TAX":"TAXE SUR LE LOGEMENT", 
                 "PAYROLL INCOME TAXES":"IMPÃ”TS SUR LE REVENU DE LA PAIE","INCOME TAX-PAS":"IMPÃ”T SUR LE REVENU-PAS", "IC SETTLEMENT":"RÃ¨glement Interentreprises",
                 "VACATION TAKEN":"VACANCES PRISES", "SOCIAL SECURITY: APPR. CONTR.":"SÃ‰CURITÃ‰ SOCIALE: CONTRIBUTION Ã€ Lâ€™APPRENTISSAGE", 
                  "POST OF AVRIL DEC IN CORRECT SIGN":"CORRECTION D'ECRITURE AVRIL DEC"}



    gl = gl.replace({"JournalLib":mapping_Valuation1}, regex=True)
    gl = gl.replace({"JournalLib":mapping_AA1}, regex=True)
    gl['JournalLib'] = gl["JournalLib"].str.replace('COST-PLUS', 'Revient MajorÃ©')
    gl['JournalLib'] = gl["JournalLib"].str.replace('PRITVAE HEALTH: MEDICAL INSURANCE', 'SANTÃ‰ PRIVÃ‰E: ASSURANCE MÃ‰DICALE')
    gl['JournalLib'] = gl["JournalLib"].str.replace('MEDICAL INSURANCE', 'ASSURANCE MÃ‰DICALE')
    gl['JournalLib'] = gl["JournalLib"].str.replace('UNASSIGNED', 'NON ATTRIBUÃ‰')
    gl['JournalLib'] = gl["JournalLib"].str.replace('Payout', 'Paiement')
    gl['JournalLib'] = gl["JournalLib"].str.replace('FRINGE COST', 'COÃ›T MARGINAL')
    gl['JournalLib'] = gl["JournalLib"].str.replace('PROJECT INITIATION', 'LANCEMENT DU PROJET')
    gl['JournalLib'] = gl["JournalLib"].str.replace('ACCRUAL', 'ACCUMULATION')
    gl['JournalLib'] = gl["JournalLib"].str.replace('CREDITCARD', 'CARTE DE CRÃ‰DIT')
    gl['JournalLib'] = gl["JournalLib"].str.replace('ACCR ', 'ACCUM ')
    gl['JournalLib'] = gl["JournalLib"].str.replace('VAT ', 'TVA ')
    gl['JournalLib'] = gl["JournalLib"].str.replace('SOCIAL SECURITY ', 'SÃ‰CURITÃ‰ SOCIALE')
    gl['JournalLib'] = gl["JournalLib"].str.replace('SEPTEMBER', 'SEPT')
    gl['JournalLib'] = gl["JournalLib"].str.replace('TAXBACK', 'Reboursement')
    gl['JournalLib'] = gl["JournalLib"].str.replace('REPORT', '')
    gl['JournalLib'] = gl["JournalLib"].str.replace("Reverse Posting", "Contre Passation d'Ecriture")
    gl['JournalLib'] = gl["JournalLib"].str.replace("BASE RENT", "Location Base")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Rent ", "Location ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RENT ", "Location ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CLEARING", "compensation ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("clearing", "compensation ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("BILLING CHARGES", "FRAIS DE FACTURATION ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("UNPAID", "NON PAYÃ‰")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PROPERTY TAX", "IMPÃ”T FONCIER ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Trans. Using", "Conversion sur")
    gl['JournalLib'] = gl["JournalLib"].str.replace("SALARIES", "Salaires")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Refund", "Remboursement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("REFUND", "Remboursement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("no invoice", "pas de facture")
    gl['JournalLib'] = gl["JournalLib"].str.replace("COST-PLUS SERVICE REVENUE", "Revenus de service Revient MajorÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("SETTLEMENT", "RÃˆGLEMENT ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PURCHASE", "ACHAT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("NON-CP SETTLE", "RÃˆGLEMENT NON-CP")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PAID ", " PayÃ© ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FEES ", "Frais")

    gl['JournalLib'] = gl["JournalLib"].str.replace("January", "Janvier")
    gl['JournalLib'] = gl["JournalLib"].str.replace("February", "FÃ©vrier")
    gl['JournalLib'] = gl["JournalLib"].str.replace("March", "Mars")
    gl['JournalLib'] = gl["JournalLib"].str.replace("April", "Avril")
    gl['JournalLib'] = gl["JournalLib"].str.replace("May", "Mai")
    gl['JournalLib'] = gl["JournalLib"].str.replace("June", "Juin")
    gl['JournalLib'] = gl["JournalLib"].str.replace("July", "Juillet")
    gl['JournalLib'] = gl["JournalLib"].str.replace("September", "Septembre")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Aug.", "AoÃ»t")

    gl['JournalLib'] = gl["JournalLib"].str.replace("JANUARY", "Janvier")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FEBRUARY", "FÃ©vrier")
    gl['JournalLib'] = gl["JournalLib"].str.replace("MARCH", "Mars")
    gl['JournalLib'] = gl["JournalLib"].str.replace("APRIL", "Avril")
    gl['JournalLib'] = gl["JournalLib"].str.replace("MAY", "Mai")
    gl['JournalLib'] = gl["JournalLib"].str.replace("JUNE", "Juin")
    gl['JournalLib'] = gl["JournalLib"].str.replace("JULY", "Juillet")
    gl['JournalLib'] = gl["JournalLib"].str.replace("SEPTEMBER", "Septembre")
    gl['JournalLib'] = gl["JournalLib"].str.replace("AUGUST.", "AoÃ»t")
    gl['JournalLib'] = gl["JournalLib"].str.replace("NOVEMBER.", "Novembre")
    gl['JournalLib'] = gl["JournalLib"].str.replace("DECEMBER.", "DÃ©cembre")
    gl['JournalLib'] = gl["JournalLib"].str.replace("December", "DÃ©cembre")

    gl['JournalLib'] = gl["JournalLib"].str.replace("Feb.", "FÃ©v.")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Mar.", "Mars")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Apr.", "Avril")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Aug.", "AoÃ»t")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Aug.", "AoÃ»t")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Reverse ", "Contre-passation ")

    gl['JournalLib'] = gl["JournalLib"].str.replace("INTEREST CHARGE", "CHARGE D'INTÃ‰RÃŠT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("-SICK LEAVE PAY", "-Paiement congÃ© maladie")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RECLASSEMENTIFICATION", "RECLASSIFICATION")
    gl['JournalLib'] = gl["JournalLib"].str.replace("INSTALMENT", "VERSEMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FIRST", "1ere")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FINE LATE PAY.", "Amende pour retard de paiement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("-PATERNITY PAY", "IndemnitÃ©s de paternitÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("SOCIAL SECURITY:", "SÃ‰CURITÃ‰ SOCIALE:")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Trip from", "Voyage de:")
    gl['JournalLib'] = gl["JournalLib"].str.replace(" To ", " Ã ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Shipping", "Livraison")
    gl['JournalLib'] = gl["JournalLib"].str.replace("VOXEET INTEGRATION COSTS", "COÃ›TS D'INTÃ‰GRATION DE VOXEET")
    gl['JournalLib'] = gl["JournalLib"].str.replace("INCOME TAX", "IMPÃ”T SUR LE REVENU")
    gl['JournalLib'] = gl["JournalLib"].str.replace('Rideshare', 'Covoiturage')
    gl['JournalLib'] = gl["JournalLib"].str.replace('Travel Meals', 'Repas de Travail')
    gl['JournalLib'] = gl["JournalLib"].str.replace('Fees', 'Frais')
    gl['JournalLib'] = gl["JournalLib"].str.replace('Phone', 'TÃ©lÃ©phone')
    gl['JournalLib'] = gl["JournalLib"].str.replace("Books", "Abonnements")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Subcriptions", "Location Base")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Meals", "Repas")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Entertainment", "divertissement ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Third Party", "tiers ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Training Fees", "Frais d0 Formation")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Conferences/Tradeshows Registratio", "ConfÃ©rences/Tradeshows Enregistrement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FOR", "POUR")
    gl['JournalLib'] = gl["JournalLib"].str.replace("ROUNDING", "ARRONDISSEMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("STORAGE", "STOCKAGE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("VACATION ACCURAL", "Vacances AccumulÃ©es")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RECEIVABLE ", "Recevables")
    gl['JournalLib'] = gl["JournalLib"].str.replace("AFTER PAYOUT ", "APRÃˆS PAIEMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CLEAN UP ", "APUREMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("EMPLOYEE TRAVEL INSUR ", "ASSURANCE DE VOYAGE DES EMPLOYÃ‰S")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CORRECTION OF", "CORRECTION DE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("TAXES PAYROLL", "IMPÃ”TS SUR LA MASSE SALARIALE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("ACCOUNT", "COMPTE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("TAX", "ImpÃ´t")
    gl['JournalLib'] = gl["JournalLib"].str.replace("life disab", "IncapacitÃ© de vie")
    gl['JournalLib'] = gl["JournalLib"].str.replace("HOUSING TAX","TAXE D'HABITATION")
    gl['JournalLib'] = gl["JournalLib"].str.replace("GROSS SALARY","SALAIRE BRUT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Cleaning Services","Nettoyage")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Freight","Fret")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Membership","adhÃ©sion")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Air cooling Maintenance","Entretien de refroidissement de l'air")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Power on Demand Platform","Plateforme d'energie Ã  la demande")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Sanitaire room installation"," Installation de la salle sanitaire")
    gl['JournalLib'] = gl["JournalLib"].str.replace("subscription","abonnement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Coffee supplies "," Fournitures de cafÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Duty and Tax ","Devoir et fiscalitÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Electricity ","ElectricitÃ© ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Lunch vouchers  ","Bons dÃ©jeuner")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Security monitoring","Surveillance de la sÃ©curitÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Water", "L'EAU")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Statutory Audit", "Audit statutaire")
    gl['JournalLib'] = gl["JournalLib"].str.replace(" Meeting room screen installation", "Installation de l'Ã©cran de la salle de rÃ©union")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Water", "L'EAU")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Water", "L'EAU")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Tax Credit FY 2016", "CrÃ©dit d'impÃ´t Exercice 2016")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Bank of America Merill Lynch-T&E statement","DÃ©claration de Merill Lynch")
    gl['JournalLib'] = gl["JournalLib"].str.replace("English Translation", "Traduction anglaise")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Office Rent", "Location de Bureau")

    gl['JournalLib'] = gl["JournalLib"].str.replace("Annual Electrical Verification", "VÃ©rification Ã©lectrique annuelle ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Health costs ", "CoÃ»ts santÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Unlimited-receipt and policy audit", "VÃ©rification illimitÃ©e des reÃ§us et audites")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Water fountain ", "Fontaine d'eau")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Quartely control visit", "Visite de contrÃ´le trimestrielle")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Fire extinguishers annual check", "VÃ©rification annuelle des extincteurs")
    gl['JournalLib'] = gl["JournalLib"].str.replace("showroom rent", "location de salle d'exposition")
    gl['JournalLib'] = gl["JournalLib"].str.replace("AND ACTUAL RECEIV","ET RECETTES RÃ‰ELLES")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FILING","DÃ‰PÃ”T")
    gl['JournalLib'] = gl["JournalLib"].str.replace("ORDERS","ORDRES")
    gl['JournalLib'] = gl["JournalLib"].str.replace("EXCLUDED -DUMMY CREDIT","EXCLU")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RELARING TO","RELATIF Ã€")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CLEAN UP-","APUREMENT-")
    gl['JournalLib'] = gl["JournalLib"].str.replace("2ND INSTALLEMENT","2Ã¨me versement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("DOUBLE PAYMENT","DOUBLE PAIEMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CLEAN UP-","APUREMENT-")
    gl['JournalLib'] = gl["JournalLib"].str.replace("DUTIES","DROITS")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Previous balance","Solde PrÃ©cÃ©dent")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Cash fx","Cash FX")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PAYROLL INCOME","REVENU DE PAIE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("TELEPHONE CHARGES","Frais de TÃ©lÃ©phone")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Clearing","Compensation")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Hotel","HÃ´tel")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Miscellaneous","Divers")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Corporate Card-Out-of-Poc","")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Traveling Dolby Empl","EmployÃ© itinÃ©rant de Dolby")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Tools-Equipment-Lab Supplies","Outils-Equipement-Fournitures de laboratoire")
    gl['JournalLib'] = gl["JournalLib"].str.replace("rounding","Arrondissement")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Building Supplies-Maintenance","MatÃ©riaux de construction-Entretien")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Expensed Furniture","Mobilier DÃ©pensÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Credit for Charges","CrÃ©dit pour frais")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Manual P-ment and double payment to be deduct","P-mnt manuel et double paiement Ã  dÃ©duire")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Employee insurance travel","Assurance de voyage des employÃ©s 2019")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Rent ","Location ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Lunch vouchers ","Bons dÃ©jeuner")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Store Room ","Chambre Stocke")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Evaluation ","Ã‰valuation  ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Charges ","Frais ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("On Line ","En ligne ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("/Building Supplies/Maintenance","/ MatÃ©riaux de construction / Entretien")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Music Instruments","Instruments Musicales")
    gl['JournalLib'] = gl["JournalLib"].str.replace("/Employee Awards/Recognition", "/ RÃ©compenses des employÃ©s / Reconnaissance")


    gl['JournalLib'] = gl["JournalLib"].str.replace("/Daily Allowance","/IndemnitÃ© journaliÃ¨re")

    gl['JournalLib'] = gl["JournalLib"].str.replace("RECLASS ", "RECLASSIFICATION ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Purchase Accounting", "ComptabilitÃ© d'achat")
    gl['JournalLib'] = gl["JournalLib"].str.replace( "EXPAT ", " ExpatriÃ© ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("FROM ", "DE ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("INVOICE", "FACTURE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CLEANUP", "APUREMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Repayment", "Restitution")

    gl['JournalLib'] = gl["JournalLib"].str.replace("Office Furniture", "Meubles de bureau")
    gl['JournalLib'] = gl["JournalLib"].str.replace("anti-stress treatments", "traitements anti-stress")

    gl['JournalLib'] = gl["JournalLib"].str.replace("UK Tax Return", "DÃ©cl. d'impÃ´t Royaume-Uni")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Office Location", "Location de bureau")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Deliver Service", "Service de livraison")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Foreign Office Support", "Soutien aux bureaux Ã©trangÃ¨res")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Showroom", "Salle d'exposition")

    gl['JournalLib'] = gl["JournalLib"].str.replace("aditional Services", "Services supplÃ©mentaires ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Cofee consumption Paris office", "Consommation de cafÃ© Bureau de Paris")

    gl['JournalLib'] = gl["JournalLib"].str.replace("Consultant ", "Expert-conseil")
    gl['JournalLib'] = gl["JournalLib"].str.replace("INVOICE", "FACTURE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Rent-", "Location-")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Corporate", "Entreprise")
    gl['JournalLib'] = gl["JournalLib"].str.replace("COST ", "COÃ›T ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("TRAINING", "Formation")
    gl['JournalLib'] = gl["JournalLib"].str.replace("LIFE DISAB", "InvaliditÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("INSU ", "ASSURANCE ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PATENT AWARD", "BREVET")

    gl['JournalLib'] = gl["JournalLib"].str.replace("EQUIVALENT POUR UNUSED VACATION POUR LEAVE", "CONGÃ‰ DE VACANCES INUTILISÃ‰S")
    gl['JournalLib'] = gl["JournalLib"].str.replace("SPOT ", "")
    gl['JournalLib'] = gl["JournalLib"].str.replace("AIRFARE TRANSFER TO PREPAIDS", "TRANSFERT DE TRANSPORT AÃ‰RIEN Ã€ PAYÃ‰ D'AVANCE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("WITHHOLDING", "RETRAIT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Clear ", "Reglement ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Clear ", "Reglement ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Rent/", "Location/")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Pay ", "Paiement ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PAYMENT", "Paiement ")

    gl['JournalLib'] = gl["JournalLib"].str.replace("French Income Tax Return;", "DÃ©claration de revenus franÃ§aise;")
    gl['JournalLib'] = gl["JournalLib"].str.replace("REVESERVICES", "SERVICES")
    gl['JournalLib'] = gl["JournalLib"].str.replace("INCLUDED DOUBLE", "DOUBLE INCLUS")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Bank", "Banque")
    gl['JournalLib'] = gl["JournalLib"].str.replace("/Promotional Expenses", "/Frais de promotion")

    gl['JournalLib'] = gl["JournalLib"].str.replace(" ACTIVITY ", " activitÃ© ")
    gl['JournalLib'] = gl["JournalLib"].str.replace(" DEFINED BENEFIT LIABILITY", "PASSIF Ã€ AVANTAGES DÃ‰TERMINÃ‰ES")
    gl['JournalLib'] = gl["JournalLib"].str.replace("COÃ›T PLUS ", "Revient MajorÃ©")
    gl['JournalLib'] = gl["JournalLib"].str.replace("/Airline Frais", "/Tarifs aÃ©riens")
    gl['JournalLib'] = gl["JournalLib"].str.replace("/Tools/Equipment/Lab Supplies", "/Outils / Ã‰quipement / Fournitures de laboratoire")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Rent/", "Location/")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Payment Posting", "Paiements")
    gl['JournalLib'] = gl["JournalLib"].str.replace("COMMISSION Dâ€™ACCUMULATION", "ACCUMULATIONS DE COMISSIONS")
    gl['JournalLib'] = gl["JournalLib"].str.replace("ImpÃ´tE", "ImpÃ´t")
    gl['JournalLib'] = gl["JournalLib"].str.replace("MED.INSU", "MED.ASSURANCE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("APPRENTICESHIP_CONTRIBUTIONS_TRUE_UP", "CONTRIBUTIONS Ã€ L'APPRENTISSAGE/TRUE UP")
    gl['JournalLib'] = gl["JournalLib"].str.replace("NET PAY", "SALAIRE NET")
    gl['JournalLib'] = gl["JournalLib"].str.replace("CASH ", "ARGENT ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Repayment ", "Repaiement ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Acct. ", "Comptab. ")

    gl['JournalLib'] = gl["JournalLib"].str.replace("ACCR ", "ACC ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Accr ", "Acc.")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Cash Balance", "Solde de caisse")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RECLASS ", "RECLASSEMENT ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("VAT FILING ", "DÃ©pÃ´t de TVA ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Needs to be re-booked due", "KI")
    gl['JournalLib'] = gl["JournalLib"].str.replace("reclass from", "reclasser de")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RECLASS FROM", "reclasser de")
    gl['JournalLib'] = gl["JournalLib"].str.replace("PAYROLL", "PAIE")
    gl['JournalLib'] = gl["JournalLib"].str.replace("RECLASS ", "Reclasser")

    gl['JournalLib'] = gl["JournalLib"].str.replace("DEDICTION","DEDUCTION")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Cash","Argent ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("cash ","argent ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("ReclasserIFICATIO","RECLASSEMENT ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("ImpÃ´tS ","ImpÃ´ts ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Working Repas (Employees Only) ","Repas de travail (employÃ©s seulement) ")
    gl['JournalLib'] = gl["JournalLib"].str.replace("/Banque Frais","/Frais Bancaires")
    gl['JournalLib'] = gl["JournalLib"].str.replace("MED. INS.","ASSURANCE MED.")
    gl['JournalLib'] = gl["JournalLib"].str.replace("AJE WIRE LOG TRAN","AJE VERSEMENT")
    gl['JournalLib'] = gl["JournalLib"].str.replace("JUN'","JUIN'")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Deferred Rent18 rue de Lo'","Loyer diffÃ©rÃ© 18 Rue de Lo'")
    gl['JournalLib'] = gl["JournalLib"].str.replace("Facture - Brut'","Facture - Brute'")


    gl['DocDate'] = gl['Document Date']

    gl.loc[gl["PieceRef"].isnull(),'PieceRef'] = gl["JournalLib"].map(str) + " " + gl.DocDate.dt.strftime('%Y%m%d').astype(str)

    gl['Document Date'] = gl['DocDate']
    del gl['DocDate']
    gl['EcritureLib'] = gl['EcritureLib'].apply(lambda x: x.upper())

    return gl



def save_results(df):
    writer = pd.ExcelWriter("sample.xlsx",
                        engine='xlsxwriter',
                        datetime_format='yyyymmdd',
                        date_format='yyyymmdd')

    df.to_excel(writer, sheet_name = ('Sheet 1'))


    workbook  = writer.book
    worksheet = writer.sheets['Sheet 1']
    worksheet.set_column('B:C', 20)
    writer.save()

if __name__ == '__main__':
    args = parse_args()
    
    gl_items = args.data_file
    parked = args.parked_and_noted
    delete = args.deleted_items
    
    output_df = combine(gl_items,parked,delete)
    print("Reading data and combining with parked and deleted items")
    print("Separating Debits and Credits")
    print("Mapping Vendors")
    output_df_translated = transform(output_df)
    print("Translating to French")
    print("Mapping French Accounts")
    print("Filling in blanks")
    save_results(output_df_translated)
    print("Done")
    print("Your file is called: sample and is located in the Downloads folder")

