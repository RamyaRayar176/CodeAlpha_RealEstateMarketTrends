import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_real_estate_data(num_records=1000):
    """Generates synthetic real estate market data."""
    
    np.random.seed(42)
    
    # Locations: Region, Approx Lat/Lon center
    regions = {
        'Downtown': (40.7128, -74.0060),
        'Suburbs': (40.7500, -74.1000),
        'Coastal': (40.6000, -73.9500),
        'Industrial': (40.8000, -74.2000),
        'Tech Park': (40.6500, -74.0500)
    }
    
    data = []
    
    start_date = datetime(2023, 1, 1)
    
    for _ in range(num_records):
        region_name = np.random.choice(list(regions.keys()))
        base_lat, base_lon = regions[region_name]
        
        # Add random jitter to location
        lat = base_lat + np.random.normal(0, 0.02)
        lon = base_lon + np.random.normal(0, 0.02)
        
        # Date
        days_offset = np.random.randint(0, 365 * 2) # 2 years of data
        date = start_date + timedelta(days=days_offset)
        
        # Property Type
        prop_type = np.random.choice(['Apartment', 'Villa', 'Commercial', 'Studio'])
        
        # Price and Yield Logic
        base_price = {
            'Apartment': 500000, 'Villa': 1200000, 
            'Commercial': 2000000, 'Studio': 300000
        }[prop_type]
        
        # Adjust price by region
        region_mult = {
            'Downtown': 1.5, 'Coastal': 1.3, 'Tech Park': 1.2,
            'Suburbs': 0.9, 'Industrial': 0.8
        }[region_name]
        
        price = base_price * region_mult * np.random.normal(1, 0.1)
        
        # Rental Yield (Inverse to price usually, but varies)
        yield_base = {
            'Downtown': 0.04, 'Coastal': 0.05, 'Tech Park': 0.06,
            'Suburbs': 0.055, 'Industrial': 0.07
        }[region_name]
        
        rental_yield = yield_base * np.random.normal(1, 0.1)
        
        # Market Conditions
        demand_score = np.random.randint(1, 100)
        supply_score = np.random.randint(1, 100)
        
        # Eco Indicator (e.g., Interest Rate effect)
        eco_indicator = np.random.normal(0.5, 0.1) 
        
        data.append({
            'Date': date,
            'Region': region_name,
            'Latitude': lat,
            'Longitude': lon,
            'Property_Type': prop_type,
            'Price': round(price, 2),
            'Rental_Yield_Pct': round(rental_yield * 100, 2),
            'Demand_Score': demand_score,
            'Supply_Score': supply_score,
            'Economic_Indicator': round(eco_indicator, 2)
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating data...")
    df = generate_real_estate_data(2000)
    output_path = "real_estate_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    print(df.head())
