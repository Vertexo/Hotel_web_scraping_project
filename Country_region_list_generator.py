# TODO: Code to generate column of all unique country names.

import pandas as pd
import os


directory = os.path.dirname(__file__)
folder_path = directory + os.path.sep + 'All_countries_in_one_file/All_country_data.xlsx'
data = pd.read_excel(folder_path)
data = data['Country']
data = data.drop_duplicates()
data.to_excel('Country_region_list.xlsx')

