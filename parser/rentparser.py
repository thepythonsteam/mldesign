import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from constants import *
import csv
import json

from tqdm import tqdm
import time
from random import seed
from random import random
from random import randint

class ParserRentOffers:
    def __init__(self, min_area: int, max_area: int, location_id: str):
        self.session = requests.Session()
        self.session.headers = {
            'Accept-Language': 'ru', 
            'User-Agent': UserAgent().random
        }
        self.result = []
        self.min_area = min_area
        self.max_area = max_area
        self.location_id = location_id
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
        # print(self.url)
        res = self.session.get(url=self.url)
        res.raise_for_status()
        return res.text

    @staticmethod
    def csv_writer(data):
        with open('дизайнерский_ремонт.csv', 'a', encoding='utf-8', errors='replace') as f:
            fieldnames = [
                'id',
                'date',
                'title',
                'price',
                'sqr_total',
                'address',
                'latitude',
                'longitude',
                'url',
                'description',
                'photos'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(data)

    def parse_page(self, html: str):
        soup = BeautifulSoup(html, 'lxml')
        ads = soup.findAll('div', {'class': '_93444fe79c--commercialWrapper--vwmUi'})
        
        try:
            show_more = soup.find('div', {'class': '_93444fe79c--moreSuggestionsButtonContainer--h0z5t'})
        except:
            current_page = int(soup.find('div', {'data-name': 'Pagination'})\
                        .find('li', {'class': '_93444fe79c--list-item--FFjMz _93444fe79c--list-item--active--WifA5'}).text)
        i = 0
        for ad in ads:
            try:
                ad_url = ad.find('a', {'class': 'c6e8ba5398--header-link--xVxAx'}).get('href') 
            except:
                continue
            ad_html = self.get_html(ad_url)
            try:
                ad_soup = BeautifulSoup(ad_html, 'lxml')
            except:
                ad_soup = BeautifulSoup(ad_html, 'lxml.parser')
            try:
                temp = ad_soup.findAll('script', {'type': 'text/javascript'})[5].decode_contents().strip()
            except:
                continue
            temp = temp.split('window._cianConfig[\'frontend-offer-card\'] = ')[1]
            temp = temp[1:-2]
            res = json.loads(
                temp[temp.find('"defaultState"') - 7:].split(',{"key":"subdomain","value"')[0]
            )['value']['offerData']['offer']
            try:
                photos = []
                for photo in res['photos']:
                    photos.append(photo['fullUrl'])
                photos = ', '.join(photos)
            except:
                # Если фоток нет, то значит, что объявление уже снято с публикации
                continue
            ad_id = res['id']
            date = res['editDate']
            title = res['title']
            geo = res['geo']['coordinates']
            address = []
            for address_element in res['geo']['address']:
                address.append(address_element['shortName'])
            address = ', '.join(address)
            latitude = geo['lat']
            longitude = geo['lng']
            description = res['description'].replace('\n', '')
            
            if res['areaParts']:
                for area in res['areaParts']:
                    price = area['price'] / area['area'] * 12
                    sqr_total = area['area']
                    data = {
                        'id': ad_id,
                        'date': date,
                        'title': title,
                        'price': price,
                        'sqr_total': area,
                        'address': address,
                        'latitude': latitude,
                        'longitude': longitude,
                        'url': ad_url,
                        'description': description,
                        'photos': photos
                    }
                    self.csv_writer(data)
                
            else: 
                price = res['pricePerUnitAreaPerYear']
                sqr_total = float(res['totalArea'])
                data = {
                    'id': ad_id,
                    'date': date,
                    'title': title,
                    'price': price,
                    'sqr_total': sqr_total,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                    'url': ad_url,
                    'description': description,
                    'photos': photos,
                }
                self.csv_writer(data)

            i += 1
        
            value = random()
            scaled_value = (1 + (value * (9 - 5))) 
            time.sleep(scaled_value)
            
        return current_page
           
    def get_results(self):
        return self.result

    def run(self):
        print(f"\n{' '*15}Start collection information from pages..")
        
        for number_page in range(1, 54):
            try: 
                # print(f"Parsing page № {number_page}")
                html = self.load_page(number_page=number_page)
                current_page = self.parse_page(html=html)
                if current_page != number_page:
                    break
            except:
                print(f"Do not exist this {number_page} page.. Ending parse\n")
            # html = self.load_page(number_page=number_page)
            # current_page = self.parse_page(html=html)
            # if current_page != number_page:
            #     break