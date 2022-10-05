import rentparser
import rentparset_v2
from constants import CITIES
from tqdm import tqdm
import time


for city in tqdm(CITIES):
    city_name = city[0]
    city_id = city[1]
    print()
    print(f'Parsing city {city_name}, please wait for a while...')
    parser = rentparset_v2.ParserRentOffers(min_area=120, max_area=900, location_id=city_id, city_name=city_name)
    try: 
        parser.run()
    except: 
        time.sleep(5)
        parser.run()
    


# parser = rentparser.ParserRentOffers(min_area=20, max_area=80, location_id=4923, start_page=1)

parser.run() 



