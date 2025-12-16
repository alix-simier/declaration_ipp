import pandas as pd
import numpy as np

def declarations_ipp(plateaux_file, ref_file, output_file=None):
    plateaux = pd.read_excel(plateaux_file, sheet_name='IPP')
    ref = pd.read_excel(ref_file)

    plateaux['Client'] = plateaux['Client'].str.strip()
    ref['ID recipient'] = ref['ID recipient'].str.strip()

    final = plateaux.merge(ref, left_on='Client', right_on='ID recipient', how='left')

    final.drop(columns=['ID recipient'], inplace=True)
    final['File Nr'] = final.index + 1
    final['Row Nr'] = final.index + 1
    final['Palletpool ID sender'] = "SCICA Gerfruit"
    final['Palletpool ID recipient'] = ""
    final['Direction'] = "D"

    conditions = [
        final['Palette'].str.contains('80X120', na=False),
        final['Palette'].str.contains('100X120', na=False),
        final['Palette'].str.contains('60X80', na=False)
    ]
    valeurs = ['E812', 'P1210', 'D608']
    final['Product'] = np.select(conditions, valeurs, default='erreur')

    final = final.rename(columns={
        'Nb. Palettes': 'Quantity',
        'N° commande': 'Reference',
        'Date chargement': 'Date Dispatched',
        'Client' : 'ID recipient'
    })

    columns = ['File Nr', 'Row Nr', 'Palletpool ID sender', 'Palletpool ID recipient', 'ID recipient',
               'Name', 'Street','Street2','Zipcode','City','Country','Contact','Telephone','Fax','E-mail',
               'Reference','Date Dispatched','Product','Quantity','Direction']

    new = final[columns].copy()

    new['Date Dispatched'] = pd.to_datetime(new['Date Dispatched'], errors='coerce')
    new['Date Dispatched'] = new['Date Dispatched'].dt.strftime('%d/%m/%Y')

    new = new[
        new['Reference'].notna() &
        (new['Reference'].astype(str).str.strip() != '')
    ]

    if output_file:
        new.to_excel(output_file, index=False)

    return new
