import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from constants import *
from constants import BASE_LINK
import csv
import json
import re
import time
from random import seed
from random import random
from random import randint

class ParserRentOffers:
    def __init__(self, min_area: int, max_area: int, location_id: str, city_name: str):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': UserAgent().random}
        self.result = []
        self.min_area = min_area
        self.max_area = max_area
        self.location_id = location_id
        self.city_name = city_name
#         self.start_page = start_page
#         self.end_page = end_page

    def build_url(self):
        return BASE_LINK

    @staticmethod
    def get_html(url): 
        r = requests.get(url)
        return r.text


    def load_page(self, number_page=1):           
        self.url = self.build_url().format(
            self.max_area, 
            self.min_area, 
            number_page, 
            self.location_id
        )
        res = self.session.get(url=self.url)
        res.raise_for_status()
        return res.text

    @staticmethod
    def csv_writer(data):
        with open('output/ads_moscow_8_11_2022.csv', 'a', encoding='utf-8', errors='replace') as f:
            fieldnames = [
                'id',
                'date',
                'region',
                'city',
                'address',
                'price',
                'sqr_total',
                'latitude',
                'longitude',
                'build_year',
                'url',
                'description',
                'photos'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(data)

    def parse_page(self, html: str):
        soup = BeautifulSoup(html, 'lxml')
        # ads = soup.findAll('div', {'class': '_93444fe79c--commercialWrapper--vwmUi'})
        try:
            current_page = int(soup.find('div', {'data-name': 'Pagination'})\
                        .find('li', {'class': '_32bbee5fda--list-item--FFjMz _32bbee5fda--list-item--active--WifA5'}).text)
        except:
            current_page = None
        t = soup.findAll('script', {'type': 'text/javascript'})[4].decode_contents().strip().split("window._cianConfig['legacy-commercial-serp-frontend'] = ")[1]
        t = t[1:-2]
        ads = json.loads(t[[m.start() for m in re.finditer('"offers"', t)][0] + 9: ].split("aggregatedOffers")[0][:-2])
        for res in ads:
            try:
                photos = []
                for photo in res['photos']:
                    photos.append(photo['fullUrl'])
                photos = ', '.join(photos)
            except:
                # Если фоток нет, то значит, что объявление уже снято с публикации
                continue
            ad_url = res['fullUrl']
            ad_id = res['id']
            date = res['creationDate']
            # title = res['title']
            if self.city_name in ['Москва', 'Санкт-Петербург']:
                city = self.city_name
            else:
                city = res['geo']['address'][1]['fullName']
            address = res['geo']['userInput']
            latitude = res['geo']['coordinates']['lat']
            longitude = res['geo']['coordinates']['lng']
            build_year = res['building']['buildYear']
            description = res['description'].replace('\n', ' ')
            # print(res)
            if res['areaParts']:
                for area in res['areaParts']:
                    price = int(area['price'] / area['area'])
                    sqr_total = area['area']
                    if self.min_area < sqr_total < self.max_area:
                        data = {
                            'id': ad_id,
                            'date': date,
                            'region': self.city_name,
                            'city': city,
                            'address': address,
                            'price': price,
                            'sqr_total': sqr_total,
                            'latitude': latitude,
                            'longitude': longitude,
                            'build_year': build_year,
                            'url': ad_url,
                            'description': description,
                            'photos': photos
                        }
                        self.csv_writer(data)
                
            else: 
                price = int(res['pricePerUnitAreaPerYearRur'] / 12)
                # price = None
                sqr_total = float(res['totalArea'])
                if self.min_area < sqr_total < self.max_area:
                    data = {
                        'id': ad_id,
                        'date': date,
                        'region': self.city_name,
                        'city': city,
                        'address': address,
                        'price': price,
                        'sqr_total': sqr_total,
                        'latitude': latitude,
                        'longitude': longitude,
                        'build_year': build_year,
                        'url': ad_url,
                        'description': description,
                        'photos': photos,
                    }
                    self.csv_writer(data)

        return current_page
           
    def get_results(self):
        return self.result

    def run(self):
        print(f"\n{' '*15}Start collection information from pages..")
        
        for number_page in range(1, 54):
            # html = self.load_page(number_page=number_page)
            # current_page = self.parse_page(html=html)
            # print(current_page)
            # if current_page != number_page or current_page == None:
            #     break
            ###########
            try: 
                # print(f"Parsing page № {number_page}")
                html = self.load_page(number_page=number_page)
                current_page = self.parse_page(html=html)
                if current_page != number_page or current_page == None:
                    break
                # value = random()
                # scaled_value = (1 + (value * (9 - 5))) * 0.5
                # time.sleep(scaled_value)
            except:
                # time.sleep(5)
                print(f"Do not exist this {number_page} page.. Ending parse\n")
            #########
            # html = self.load_page(number_page=number_page)
            # current_page = self.parse_page(html=html)
            # if current_page != number_page:
            #     break
