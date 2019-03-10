# TODO: booking.com file combiner code.

import pandas as pd
import os


directory = os.path.dirname(__file__)
folder_path = directory + os.path.sep + 'cleaned_country_files'
file_name_list = os.listdir(folder_path)   # == ['1_Afghanistan_booking.com_clean.xlsx', '2_Albania_booking.com_clean.xlsx', ...,]

appended_data = []
for country_file in file_name_list:
    data = pd.read_excel(folder_path + os.path.sep + country_file)
    appended_data.append(data)

appended_data = pd.concat(appended_data, axis=0)

appended_data['Breakfast included'][appended_data['Breakfast included'] == 1] = True
final_df = appended_data.sort_values('Country ID')

writer = pd.ExcelWriter('All_countries_in_one_file/All_country_data.xlsx', options={'strings_to_urls': False})
final_df.to_excel(writer)
writer.save()
