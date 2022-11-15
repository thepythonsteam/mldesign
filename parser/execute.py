import parse_commercial
import parse_flats
from constants import CITIES
from tqdm import tqdm
import time

def main():
    for city in tqdm(CITIES):
        city_name = city[0]
        city_id = city[1]
        print()
        print(f'Parsing city {city_name}, please wait for a while...')
        parser_instance = parse_flats.ParserRentOffers(min_area=1, max_area=80, location_id=city_id, city_name=city_name)
        try: 
            parser_instance.run()
        except: 
            time.sleep(5)
            parser_instance.run()


if __name__ == '__main__':
    main()