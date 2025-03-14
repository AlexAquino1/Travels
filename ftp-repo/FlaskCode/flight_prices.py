import requests, json
import os
from dotenv import load_dotenv

load_dotenv()
flightapi = os.getenv('flightapi')


#from flask_caching import Cache
#cache = Cache(config={'CACHE_TYPE': 'simple'})

#@cache.memoize(timeout=60)
def flightPrices(origin, destination,origin_dict,destination_dict, depart, return1, adults, children, infants, cabinClass, sortBy, maxPrice=None, minPrice=None):
    url = "https://skyscanner50.p.rapidapi.com/api/v1/searchFlights"
    
    querystring = {
        "origin": origin_dict,
        "destination": destination_dict,
        "date": depart,
        "returnDate": return1,
        "adults": adults,
        "children": children,
        "infants": infants,
        "cabinClass" : cabinClass,
        "filter" : sortBy,
        "currency": "USD",
        "countryCode": "US",
        "market": "en-US"
    }
    headers = {
        "X-RapidAPI-Key": flightapi,
        "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
    }

    response = requests.get(url, params=querystring, headers=headers, timeout=30)

    try:
        data = response.json()['data']
    except KeyError:
        print("Error: Failed to retrieve flight data")
        return []
    
    print(data)
    results = []
    for item in data:
        
        price = float(item['price']['amount'])
        if (maxPrice is None or price <= float(maxPrice)) and (minPrice is None or price >= float(minPrice)):
            flight = {
                'Id': item['id'],
                'Price': item['price']['amount'],
                'Origin': item['legs'][0]['origin']['name'],
                'Destination': item['legs'][0]['destination']['name'],
                'Departure': item['legs'][0]['departure'],
                'Arrival': item['legs'][0]['arrival'],
                'Duration': item['legs'][0]['duration'],
                'Carrier': item['legs'][0]['carriers'][0]['name'],
                'Stops': item['legs'][0]['stop_count'],
                'Adults':adults,
                'Children':children,
                'Infants':infants
                }
            if len(item['legs']) > 1:
                    flight['ConnectingOrigin'] = item['legs'][1]['origin']['name']
                    flight['ConnectingDestination'] = item['legs'][1]['destination']['name']
                    flight['ConnectingDeparture'] = item['legs'][1]['departure'] 
                    flight['ConnectingArrival'] = item['legs'][1]['arrival'] 
                    flight['ConnectingDuration'] = item['legs'][1]['duration'] 
                    flight['ConnectingCarrier'] = item['legs'][1]['carriers'][0]['name']
                    flight['ConnectingStops'] = item['legs'][1]['stop_count']

            results.append(flight)

    return results
#@cache.memoize(timeout=60)
def search_airport(user_input):
    url = "https://skyscanner50.p.rapidapi.com/api/v1/searchAirport"

    querystring = {"query": user_input}

    headers = {
        "X-RapidAPI-Key": flightapi,
        "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
 
    iata_code = data[1]['PlaceId']
    airport_dict = {'PlaceId': iata_code}

    return airport_dict
def returnFlightUrl(id,origin, destination, depart, arrival,adults,children,infants,price):
    url = "https://skyscanner50.p.rapidapi.com/api/v1/getFlightDetails"
    legs = [{"origin": origin, "destination": destination, "date": depart},
            {"origin": destination, "destination": origin, "date": arrival}]
    print(legs)
    querystring = {"itineraryId":id,
                   "legs":json.dumps(legs),
                   "adults":adults,
                   "children":children,
                   "infants":infants,
                   "currency":"USD",
                   "countryCode":"US",
                   "market":"en-US"}

    headers = {
	    "X-RapidAPI-Key": flightapi,
	    "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
        }
    response = requests.get(url, params=querystring, headers=headers, timeout=60)
    try:
     data = response.json()['data']
    except KeyError:
        print("Error: Failed to retrieve flight data")
        return []
    flightURL = data['pricingOptions'][0]['agents'][0]['url']
    #search data for pricing
    #for item in data['pricingOptions']:
    #    if flightURL != "":
    #        if float(item['totalPrice']) == float(price):
    #            flightURL = item['agents'][0]['url']
    #    else:
    #        break
    print(f"FlightURL: {flightURL}")
    return flightURL