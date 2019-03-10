#TODO: RCS end project web scraping test code.

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as soup
import time
import pandas as pd



options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

for i in range(202, 203):   # Inspecting booking.com dest_id parameter, it is clear that there is 1-254 country ids.

    # dest_id 150, 234, 246, 247, 248, 249 does not exist.
    absent_dest_id_list = [150, 234, 246, 247, 248, 249]
    if i in absent_dest_id_list:
        continue


    # Parameters for URL.
    dest_id = str(i)
    checkin = '2019-02-20'
    checkout = '2019-02-21'
    # nr_rows = '50'
    offset = '0'
    no_rooms = '1'
    group_adults = '1'
    group_children = '0'

    url = f"https://www.booking.com/searchresults.html?dest_id={dest_id};dest_type=country;checkin={checkin};checkout={checkout};offset={offset};no_rooms={no_rooms};group_adults={group_adults};group_children={group_children}"

    driver.get(url)

    element = driver.find_element_by_id('right')

    main_div = element.get_attribute('innerHTML')

    main_div_soup = soup(main_div, 'html.parser')
    text_header = main_div_soup.find('h1')

    country = text_header.text.split(":")[0].replace('\n', '')
    number_of_hotels = int(text_header.text.split(": ")[1].split(' ')[0].replace(',', ''))

    print(dest_id, ' ', country)
    print(number_of_hotels, '\n')


    number_of_hotels_list = []
    checkin_date_list = []
    checkout_date_list = []
    country_list = []
    country_ID_list = []
    hotel_name_list = []
    hotel_ID_list = []
    hotel_link_list = []
    latitude_list = []
    longitude_list = []
    hotel_stars_list = []
    hotel_review_score_list = []
    hotel_review_count_list = []
    hotel_price_list = []
    breakfast_included_list = []


    hotel_div_list = []
    nothing_found = []
    count = 0
    while int(offset) < 2200:

        offset = str(int(offset) + len(hotel_div_list))

        url = f"https://www.booking.com/searchresults.html?dest_id={dest_id};dest_type=country;checkin={checkin};checkout={checkout};offset={offset};no_rooms={no_rooms};group_adults={group_adults};group_children={group_children}"


        # Put code to sleep for n seconds.
        time.sleep(1)


        driver.get(url)

        element = driver.find_element_by_id('right')

        main_div = element.get_attribute('innerHTML')

        main_div_soup = soup(main_div, 'html.parser')


        hotel_div_list = main_div_soup.find_all('div', {'class': 'sr_item_content'})
        print('len(hotel_div_list) = ', len(hotel_div_list))
        if len(hotel_div_list) == 0:
            break

        hotel_photo_html_list = main_div_soup.find_all('div', {'class': 'sr_item_photo'})



        for photo_html in hotel_photo_html_list:
            hotel_ID_list.append(int(str(photo_html).split('id="hotel_')[1].split('"')[0]))


        print('offset = ', offset)

        hotel_price_html_list = []
        for hotel_div in hotel_div_list:
            count += 1
            print(count)

            number_of_hotels_list.append(int(number_of_hotels))
            checkin_date_list.append(checkin)
            checkout_date_list.append(checkout)
            country_list.append(country)
            country_ID_list.append(int(dest_id))

            hotel_title_html = hotel_div.find('h3', {'class': 'sr-hotel__title'})
            hotel_name_html = hotel_title_html.find('span', {'class': 'sr-hotel__name'})

            hotel_name_list.append(hotel_name_html.text.replace('\n', ''))
            long_link = 'https://www.booking.com' + str(hotel_title_html.find('a')['href'].replace('\n', ''))
            hotel_link_list.append(long_link.split("html?")[0] + 'html')

            hotel_stars_html = hotel_div.find('i', {'class': 'bk-icon-stars'})
            if hotel_stars_html is not None:
                hotel_stars = (str(hotel_stars_html).split('-sprite-ratings_stars_')[1].split('"')[0])
                if 'half' in hotel_stars:
                    hotel_stars = int(hotel_stars.split('_')[0]) + 0.5

                hotel_stars_list.append(int(hotel_stars))
            else:
                hotel_stars_list.append(None)


            hotel_coord_html = hotel_div.find('div', {'class': 'address'})
            longitude_latitude_list = str(hotel_coord_html).split('data-coords="')[1].split('"')[0].split(',')
            latitude_list.append(float(longitude_latitude_list[1]))
            longitude_list.append(float(longitude_latitude_list[0]))


            hotel_review_score_html = hotel_div.find('div', {'class': 'bui-review-score__badge'})
            if hotel_review_score_html is not None:
                hotel_review_score_list.append(float(str(hotel_review_score_html).split('aria-label="')[1].split('"')[0]))
            else:
                hotel_review_score_list.append(None)


            hotel_review_count_html = hotel_div.find('div', {'class': 'bui-review-score__text'})
            if hotel_review_score_html is not None:
                hotel_review_count_list.append(int(str(hotel_review_count_html).split('bui-review-score__text"> ')[1].split(' ')[0].replace(',', '')))
            else:
                hotel_review_count_list.append(None)


            hotel_price_html = hotel_div.find('td', {'class': 'roomPrice'})
            if hotel_price_html is not None:
                hotel_price_html_list.append(hotel_price_html.find('b'))
            else:
                hotel_price_html_list.append(None)


            breakfast_included_html = hotel_div.find('sup', {'class': 'sr_room_reinforcement'})
            if breakfast_included_html is not None:
                breakfast_included = breakfast_included_html.text.replace('\n', '')
                if breakfast_included == 'Breakfast included':
                    breakfast_included_list.append(True)
                else:
                    breakfast_included_list.append(None)
            else:
                breakfast_included_list.append(None)


        for html in hotel_price_html_list:
            digit_list = []
            if html is not None:
                for i in str(html):
                    if i.isdigit():
                        digit_list.append(i)
                hotel_price_list.append(int(''.join(digit_list)))
            else:
                hotel_price_list.append(html)



    zipped_country_hotel_data = list(zip(number_of_hotels_list, checkin_date_list, checkout_date_list, country_list, country_ID_list, hotel_name_list, hotel_ID_list, hotel_link_list, latitude_list, longitude_list, hotel_stars_list, hotel_review_score_list, hotel_review_count_list, hotel_price_list, breakfast_included_list))

    df = pd.DataFrame(zipped_country_hotel_data, columns=['Number of hotels found per country', 'Check in date', 'Check out date', 'Country', 'Country ID', 'Hotel name', 'Hotel ID', 'Booking.com hotel link', 'Latitude', 'Longitude', 'Hotel star rating', 'Review rating', 'Number of reviews', 'Price per night (Eur)', 'Breakfast included (True/False)'])

    writer = pd.ExcelWriter(f'Scraped_country_files/{dest_id}_{country}_booking.com.xlsx', engine='xlsxwriter', options={'strings_to_urls': True})
    df.to_excel(writer)
    writer.save()


driver.quit()

