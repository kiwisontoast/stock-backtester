import requests
import pandas as pd

def get_inflation_data(country='united-states'):
    url = f"https://www.statbureau.org/get-data-json?country={country}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching inflation data: {e}")
        return None

def process_inflation_data(inflation_data):
    if not inflation_data:
        return pd.Series()
    
    df = pd.DataFrame(inflation_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['InflationRate'] = df['InflationRate'] / 100  # Convert to decimal
    return df['InflationRate'].sort_index()
