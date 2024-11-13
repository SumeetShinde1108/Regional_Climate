import requests
from .models import Region, Parameter
from .utils import parse_weather_data

BASE_URL = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/date/{region}.txt"

def fetch_and_store_weather_data():
    regions = [
        'UK', 'England', 'Wales', 'Scotland', 'Northern_Ireland', 'England_and_Wales', 'England_N', 
        'England_S', 'Scotland_N', 'Scotland_E', 'Scotland_W', 'England_E_and_NE', 
        'England_NW_and_Wales_N', 'Midlands', 'East_Anglia', 'England_SW_and_Wales_S', 
        'England_SE_and_Central_S'
    ]
    parameters = ['Tmax', 'Tmin', 'Tmean', 'Sunshine', 'Rainfall']  

    for region_name in regions:
        region, _ = Region.objects.get_or_create(name=region_name)
        
        for param_name in parameters:
            parameter, _ = Parameter.objects.get_or_create(name=param_name)
            url = BASE_URL.format(parameter=param_name, region=region_name)
            response = requests.get(url)
            
            if response.status_code == 200:
                parse_weather_data(response.text, region, parameter)
            else:
                print(f"Failed to fetch data for {region_name} - {param_name}")
