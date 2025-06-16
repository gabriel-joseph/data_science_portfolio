import requests

api_key = "fH8OUy9MPiGaQRKQzwTlQ4xEgYvgfv6qPbK4RE9Z"

url = "https://api.eia.gov/v2/total-energy/data/"
params = {
    "api_key": api_key,
    "data[]": "value",
    "frequency": "annual",
    "facets[msn][]": "TETCBUS",  # Total Energy Consumption (Btu) - US
    "start": "2010",
    "end": "2023",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for point in data['response']['data']:
        print(f"Year: {point['period']}, Consumption: {point['value']}")
else:
    print("Error:", response.status_code, response.text)
    
    
