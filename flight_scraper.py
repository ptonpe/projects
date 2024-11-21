from serpapi import GoogleSearch
import csv
import json
import random
from datetime import datetime, timedelta


def get_flights_data(api_key, departure_id, arrival_id, outbound_date, return_date=None):
    # set up parameters for the SerpApi Google Flights API search
    params = {
        "api_key": api_key,
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": "USD"
    }
    
    # add return date if given
    if return_date:
        params["return_date"] = return_date

    # use GoogleSearch to get flight data
    search = GoogleSearch(params)
    results = search.get_dict()
    #print(json.dumps(results, indent=2))

    return results

def flight_data_to_csv(flights_data, filename='flights.csv'):
    # get flight details from the response
    if 'error' in flights_data:
        print(flights_data['error'])
        return
    
    flights = flights_data.get('other_flights', [])
    if not flights:
        print("No flight data found.")
        return
    
    # set up CSV columns for AI model
    columns = [
        'Airline', 'Flight Number', 'Departure City', 'Arrival City', 'Departure Date',
        'Return Date', 'Price', 'Stops', 'Duration', 'Departure Time', 'Arrival Time' 
    ]

    # open CSV file and write data in append mode
    with open(filename, mode='a+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        # write the header only if the file is empty
        file.seek(0)
        if file.read(1) == '':
            writer.writeheader()

        for flight_group in flights:
            for flight in flight_group.get('flights', []):
                writer.writerow({
                    'Airline': flight.get('airline', 'N/A'),
                    'Flight Number': flight.get('flight_number', 'N/A'),
                    'Departure City': flight.get('departure_airport', {}).get('name', 'N/A'),
                    'Arrival City': flight.get('arrival_airport', {}).get('name', 'N/A'),
                    'Departure Date': flight.get('departure_airport', {}).get('time', 'N/A'),
                    'Return Date': flights_data.get('return_date', 'N/A'),
                    'Price': flight_group.get('price', 'N/A'),
                    'Stops': len(flight_group.get('layovers', [])),
                    'Duration': flight.get('duration', 'N/A'),
                    'Departure Time': flight.get('departure_airport', {}).get('time', 'N/A'),
                    'Arrival Time': flight.get('arrival_airport', {}).get('time', 'N/A')
                })

def flight_search():
    api_key = '89dfaa5f64904dc84f63e2823f7db1a2f7583a6b3da2cd26f0fb4cd59617a3ca'

    airports = ["DFW", "SEA", "JFK", "LAX", "ORD", "MIA", "BOS", "ATL", "SFO", "DEN"]

    # Random airport search (can change for testing)
    searches = []
    for _ in range(50):
        departure_id = random.choice(airports)
        arrival_id = random.choice([airport for airport in airports if airport != departure_id])
        outbound_date = (datetime.now() + timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=random.randint(181, 365))).strftime('%Y-%m-%d')
        searches.append({"departure_id": departure_id, "arrival_id": arrival_id, "outbound_date": outbound_date, "return_date": return_date})


    # Get flight details using SerpApi
    for search in searches:
        flights_data = get_flights_data(api_key, search["departure_id"], search["arrival_id"], search["outbound_date"], search["return_date"])

        # Save flight data to CSV
        flight_data_to_csv(flights_data)

    print("Flight data saved to flights.csv")

def main():
    flight_search()

if __name__ == "__main__":
    main()
