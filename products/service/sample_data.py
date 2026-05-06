import requests
import json
import random
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

def dump_products_data():
    try:
        url = "https://fakestoreapi.com/products"
        for i in range(1, 10):
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
        
        # Modifying column names to match the database schema
        df.rename(columns={
            'title': 'name',
        }, inplace=True)
        df.drop(columns=['id', 'rating'], inplace=True)

        # adding random integer stock values using loop
        for index, row in df.iterrows():
            df.at[index, 'stock'] = int(random.randint(1, 100))
        
        # mapping category values to match the database schema choices
        def map_category(cat):
            if not isinstance(cat, str):
                return 'misc/other'
            c = cat.lower().strip()
            if 'elect' in c:
                return 'electronics'
            if 'cloth' in c or 'jewel' in c:
                return 'fashion-apparel'
            if 'home' in c or 'kitchen' in c:
                return 'home-kitchen'
            if 'toy' in c:
                return 'toys-games'
            if 'beaut' in c or 'personal' in c or 'care' in c:
                return 'beauty-personal-care'
            if 'sport' in c or 'outdoor' in c:
                return 'sports-outdoors'
            if 'book' in c:
                return 'books-media'
            if 'groc' in c or 'food' in c:
                return 'grocery-essentials'
            if 'auto' in c or 'car' in c:
                return 'automotive'
            return 'misc/other'

        df['category'] = df['category'].apply(map_category)

        df.to_csv(os.path.join(os.getcwd(), 'products', 'service', "products data.csv"), index=False)
        print("Data dumped successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":    
    dump_products_data()
