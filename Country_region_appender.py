#TODO: Add new region column. Designating region for specific country.

import pandas as pd


all_countries_df = pd.read_excel('All_countries_in_one_file/All_country_data.xlsx')
regions_df = pd.read_excel('Country_region_list.xlsx')

region_dict = dict(zip(regions_df['Country'], regions_df['Region']))

all_countries_df['Region'] = all_countries_df['Country'].map(region_dict)

all_countries_df['Breakfast included'][all_countries_df['Breakfast included'] == 1] = True
all_countries_df['Breakfast included'].fillna(False, inplace=True)

writer = pd.ExcelWriter('All_countries_in_one_file/All_country_data_plus_regions.xlsx', options={'strings_to_urls': False})
all_countries_df.to_excel(writer)
writer.save()
