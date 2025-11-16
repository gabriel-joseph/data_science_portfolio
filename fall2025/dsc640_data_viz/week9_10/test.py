import pandas as pd 

iata_icao  = pd.read_csv('iata_icao.csv')
complaints_by_subcategory  = pd.read_csv('complaints-by-subcategory.csv')
iata_complaints_by_category_icao  = pd.read_csv('complaints-by-category.csv')
complaints_by_airport  = pd.read_csv('complaints-by-airport.csv')


# take 100 rows from each dataframe and save to new CSV called sample 
iata_icao.sample(n=100, random_state=1).to_csv('sample/iata_icao.csv', index=False)
complaints_by_subcategory.sample(n=100, random_state=1).to_csv('sample/complaints_by_subcategory.csv', index=False)
iata_complaints_by_category_icao.sample(n=100, random_state=1).to_csv('sample/iata_complaints_by_category_icao.csv', index=False)
complaints_by_airport.sample(n=100, random_state=1).to_csv('sample/complaints_by_airport.csv', index=False)

print("Sample CSV files created successfully.")