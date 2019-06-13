import pandas as pd

df = pd.read_excel("2019journal.xlsx")

mapping_valuation = {"100000 - Valuation on 20181026": "100000 - Évaluation sur 20181026",
          "100000 - Valuation on 20181026 Reverse":"100000 -  Évaluation sur 20181026 Contre Passation",
           "100003 - Valuation on 20181026 Reverse":"100003 -  Évaluation sur 20181026 Contre Passation",
           "217020 - Valuation on 20181026 Reverse":"217020 -  Évaluation sur 20181026 Contre Passation",
           "200000 - Valuation on 20181026 Reverse":"200000 -  Évaluation sur 20181026 Contre Passation",
           "190010 - Valuation on 20181026 Reverse":"190010 -  Évaluation sur 20181026 Contre Passation",
           "600500 - Valuation on 20181026 Reverse":"600500 -  Évaluation sur 20181026 Contre Passation",
           "605100 - Valuation on 20181026 Reverse":"605100 -  Évaluation sur 20181026 Contre Passation",
           "600770 - Valuation on 20181026 Reverse":"600770 -  Évaluation sur 20181026 Contre Passation",
           "600900 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "635010 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "635030 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "600900 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "600900 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "600900 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "635010 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "635030 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "644020 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "645000 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "645010 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "645030 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "670020 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "670050 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "670080 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "671030 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",
           "670020 - Valuation on 20181026 Reverse":"600900 -  Évaluation sur 20181026 Contre Passation",  
    "600000 - Translation Using 20181026":"600000 - Conversion de devise sur 20181026",
           "Reverse Posting 600000 - Trans. Using 20181026":"Contre Passation d'Ecriture -  Conversion de devise sur 20181026 ",
           "600030 - Translation Using 20181026":"",
           "600040 - Translation Using 20181026":"",
           "600020 - Translation Using 20181026":"",
           "600060 - Translation Using 20181026":"",
           "600100 - Translation Using 20181026":"",
           "Reverse Posting 600020 - Trans. Using 20181026":"",
           "Reverse Posting 600030 - Trans. Using 20181026":"",
           "Reverse Posting 600040 - Trans. Using 20181026":"",
           "Reverse Posting 600060 - Trans. Using 20181026":"",
           "Reverse Posting 600100 - Trans. Using 20181026":"",
          "":"",
          "":"",
          }

df = df.replace({"Text":mapping})

print(df['Text'].head())
