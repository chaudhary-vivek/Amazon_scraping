import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import numpy as np
header = {"User-Agent": "AdsBot-Google (+http://www.google.com/adsbot.html)"}
###################################################################
url_df = pd.read_csv(r'D:\radhika\AMZ\Natural\0_AMZ_organic.csv')
#####################################################################

for i in url_df.index:
    product_list = []
    for pgno in range(200):
        
        
        pgurl = url_df.iloc[i, 1]
        filename = url_df.iloc[i, 0]
        url = pgurl + str(pgno)
        print(url)
        print(filename)
        response = requests.get(url, headers = header)
        response = response.text
        data = BeautifulSoup(response, 'lxml')
            
        all_products = data.select('.s-latency-cf-section')
           
        for product in all_products:
            try:
                name = product.select('.a-color-base.a-text-normal')[0].getText()
            except:
                name = 'NA'
            try:
                price = product.select('.a-price-whole')[0].getText()
            except:
                price = np.nan
            try:
                reviews = product.select('.a-size-small .a-size-base')[0].getText()
            except:
                reviews = 0
            prod_item = {
                        #'brand' : brand,
                        'name' : name,
                        'price' : price,
                        'reviews' : reviews
                        }
            product_list.append(prod_item)       
    df = pd.DataFrame(product_list)
    del product_list
    df = df[df['name'] != 'NA']
    df['Brand'] = df['name'].str.split(' ').str.get(0)
    df['reviews'] = df['reviews'].str.replace(',', '')
    df['reviews'] = df['reviews'].fillna(0)
    df['reviews'] = df['reviews'].astype(int)
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].fillna(0)
    df['price'] = df['price'].astype(float)
    df = df.sort_values(by = 'reviews', ascending = False)
    df.to_csv(filename +'products.csv')
    
    ####################################################################################################
    
    brands = df['Brand'].unique().tolist()
    brand_list = []
    for brand in brands :
        sub_df = df[df.Brand == brand]
        total_reviews = sub_df.reviews.sum()
        avg_price = round(sub_df.price.mean())
        listings = len(sub_df.index)
        brand_item = {
                        #'brand' : brand,
                        'name' : brand,
                        'reviews' : total_reviews,
                        'average price' : avg_price,
                        'listings' : listings
                        }
        brand_list.append(brand_item)
    brand_df = pd.DataFrame(brand_list)
    brand_df = brand_df.sort_values(by = 'reviews', ascending = False)
    del brand_list
    brand_df.to_csv(filename + '.csv')   
    


#df.to_csv('tableware.csv')