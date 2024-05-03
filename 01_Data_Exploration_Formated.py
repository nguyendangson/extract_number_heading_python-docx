# %pip install pandas
# %pip install matplotlib
# %pip install tqdm
# %pip install fpdf

import os
import re

import pandas as pd 

from tqdm import tqdm
from fpdf import FPDF
from datetime import datetime

os.getcwd()


# Import Data
original_data = pd.read_csv("./Argus_2021_2023_year_to_date.csv")

df = original_data.copy()

df['MODEL'] = ['PlaceHolder']*len(df) 

format_cols = ['SR_NUMBER', 'CREATION_DATE', 'CLOSE_DATE', 'VIN_NUMBER', 'MODEL', 'STATUS', 'SUBSTATUS', 'DESCRIPTION_COMPLAINT', 'COMMENTS']

df = df[format_cols]

df['CREATION_DATE'] = df['CREATION_DATE'].apply(lambda x: datetime.strptime(x, '%d%b%Y:%H:%M:%S.%f').strftime('%Y-%m-%d'))
df['CLOSE_DATE'] = df['CLOSE_DATE'].apply(lambda x: datetime.strptime(x, '%d%b%Y:%H:%M:%S.%f').strftime('%Y-%m-%d'))

df['SR_NUMBER'] = df['SR_NUMBER'].astype(str)
df['VIN_NUMBER'] = df['VIN_NUMBER'].astype(str)
df['MODEL'] = df['MODEL'].astype(str)
df['STATUS'] = df['STATUS'].astype(str)
df['SUBSTATUS'] = df['SUBSTATUS'].astype(str)

df['COMMENTS'] = df['COMMENTS'].astype(str)
df['DESCRIPTION_COMPLAINT'] = df['DESCRIPTION_COMPLAINT'].astype(str)

# Cleaning Data
df['DESCRIPTION_COMPLAINT'] = df['DESCRIPTION_COMPLAINT'].apply(lambda row: re.sub('\r',' ',row))
df['DESCRIPTION_COMPLAINT'] = df['DESCRIPTION_COMPLAINT'].apply(lambda row: re.sub('\n',' ',row))

df['COMMENTS'] = df['COMMENTS'].apply(lambda row: re.sub('\r',' ',row))
df['COMMENTS'] = df['COMMENTS'].apply(lambda row: re.sub('\n',' ',row))

df = df[~df.apply(lambda row: (row['DESCRIPTION_COMPLAINT'] in row['COMMENTS']) or (row['COMMENTS'] in row['DESCRIPTION_COMPLAINT'] ), axis=1)]

df = df[~df['COMMENTS'].str.contains('Action Needed')]

df = df[~df['COMMENTS'].str.contains('Correction Needed')]

df = df[~df['COMMENTS'].str.contains('Case closed due to no activity')]

df = df[~df['COMMENTS'].str.contains('Case cancelled due to no activity')]

def stopped_word(text, erase_woords):
    for w in erase_woords:
        if w in text:
            text = re.sub(w, '', text)
    return text

erase_woords = ['Case can be closed', 'case can be closed', 'No problem, closing the case', 'Please close case', 
                'ok to close', 'This case can be closed', 'Good deal, closing the case', 'case closed', 'Case closed', 'closing case',
                'Thanks you may close the case', 'Thank you', 'thank you', 'Thanks', 'thanks', 'Thank', 'thank', 'for the update',
                'Hi', 'Hello', 'hi', 'hello',
                'Best Regards', 'Have a good day', 'Sounds good']

df['COMMENTS'] = df['COMMENTS'].apply(lambda row: stopped_word(row, erase_woords))

df = df[(df['COMMENTS']!="")]

# Final Data
comments_fmt = df.groupby('SR_NUMBER')['COMMENTS'].apply(list).reset_index()
comments_fmt['COMMENTS'] = comments_fmt['COMMENTS'].apply(lambda x: [" " + str(i+1) + ". " + x[i] for i in range(len(x))])
comments_fmt['COMMENTS'] = comments_fmt['COMMENTS'].apply(lambda x: '\n'.join(x))

keep_cols = ['SR_NUMBER', 'CREATION_DATE', 'CLOSE_DATE', 'VIN_NUMBER', 'MODEL', 'STATUS', 'SUBSTATUS', 'DESCRIPTION_COMPLAINT']

df.drop_duplicates(subset='SR_NUMBER', inplace=True)

df2 = df[keep_cols].merge(comments_fmt, on='SR_NUMBER')

# Export pdfs from dataframe
# Function to build pdf with a certain format from a dataframe
def dataframe_to_pdf(df, filename):
    a4_width_mm = 210
    a4_height_mm =297
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    
    errors = []
    for ix, row in tqdm(df.iterrows(), total=len(df)):
        
        try:
            pdf.add_page()
            pdf.set_font('Arial', 'B', fontsize_pt)

            pdf.multi_cell(0, fontsize_mm + 2, 'SR-NUMBER: ' + row['SR_NUMBER'] + '\n')
            pdf.multi_cell(0, fontsize_mm + 2, 'CREATION_DATE: ' + row['CREATION_DATE'] + '\n')
            pdf.multi_cell(0, fontsize_mm + 2, 'CLOSE_DATE: ' + row['CLOSE_DATE'] + '\n')
            pdf.multi_cell(0, fontsize_mm + 2, 'VIN: ' + row['VIN_NUMBER'] + '\n')
            pdf.multi_cell(0, fontsize_mm + 2, 'MODEL: ' + row['MODEL'] + '\n\n')
            pdf.multi_cell(0, fontsize_mm + 2, 'STATUS: ' + row['STATUS'] + ' | ' + 'SUBSTATUS: ' + row['SUBSTATUS'] + '\n\n')

            pdf.set_font('Arial', 'B', fontsize_pt + 8)
            pdf.multi_cell(0, (fontsize_pt +8) * pt_to_mm, 'Technician Complaint:' + '\n\n')  

            pdf.set_font('Arial', '', fontsize_pt) 
            pdf.multi_cell(0, fontsize_mm +2, row['DESCRIPTION_COMPLAINT'].encode('utf-8').decode('latin-1') + '\n\n')

            pdf.set_font('Arial', 'B', fontsize_pt + 8)
            pdf.multi_cell(0, (fontsize_pt +8) * pt_to_mm, 'Technician Comments:' + '\n\n')

            pdf.set_font('Arial', '', fontsize_pt)
            pdf.multi_cell(0, fontsize_mm +2, row['COMMENTS'].encode('utf-8').decode('latin-1'))

        except TypeError as e:
            errors.append(ix)
           
    pdf.output(filename, 'F')
    
    return errors

# Function to export pdf for a dataframe along each row
def export_pdf(df):
    errors=[]
    for i in range(len(df)):
        start = i
        end = i+1
        tmp_df = df.iloc[start:end] 
        sr_number_name = tmp_df[0:1]['SR_NUMBER'][i]
        tmp_errors = dataframe_to_pdf(df=tmp_df, filename=f"./output_pdf/SR_NUMBER-{sr_number_name}.pdf".format(i)) 
        errors.extend(tmp_errors)
        if len(errors)>0:
            return print('There are an error at row:', i)
        
    return print('There is no error')

# Start exporting
export_pdf(df2)
