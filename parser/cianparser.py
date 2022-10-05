from rentparser import ParserRentOffers
from constants import * 


def list_cities():
    return CITIES

def parse(location, start_page=1 , end_page=1): 
    for city in CITIES: 
        if city[0] == location: 
            finded = True
            location_id = city[1]

    # if not finded: 
    #     raise ValueError(f"You entered {location} which is not exist in base")
    
    parser = ParserRentOffers(location_id=location_id, start_page=start_page, end_page=end_page)
    parser.run()
    print('\n')

    return parser.get_results()

