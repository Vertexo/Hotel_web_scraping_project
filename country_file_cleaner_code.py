# TODO: booking.com file cleaning code.

import pandas as pd
import os


directory = os.path.dirname(__file__)

folder_path = directory + os.path.sep + 'Scraped_country_files'
file_name_list = os.listdir(folder_path)   # == ['1_Afghanistan_booking.com.xlsx', '2_Albania_booking.com.xlsx', ...,]

for country_file in file_name_list:

    df = pd.read_excel(folder_path + os.path.sep + country_file)
    df = df.drop(['Number of hotels found per country'], axis=1)
    df = df.drop_duplicates(subset='Hotel ID')

    decimals = pd.Series([4, 4], index=['Latitude', 'Longitude'])
    df = df.round(decimals)

    df['Breakfast included (True/False)'][df['Breakfast included (True/False)'] == 1] = True

    df = df.rename(columns={'Breakfast included (True/False)': 'Breakfast included'})

    new_country_file_name = country_file.replace('.xlsx', '') + '_clean.xlsx'

    df.to_excel('cleaned_country_files' + os.path.sep + new_country_file_name)