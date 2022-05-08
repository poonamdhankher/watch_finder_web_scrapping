# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from re import sub
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv
from datetime import date
from socket import timeout
import urllib
from numpy import product


for  page_number in range(1, 85):
    print('Scrapping Page: ' + str(page_number))

    urlpage=urlopen("https://www.watchfinder.co.uk/new-arrivals?orderby=BestMatch&pageno="+str(page_number)).read()
    # create an array
    products = []
    soup = BeautifulSoup(urlpage, "html.parser")
    productDivs = soup.findAll('div', attrs={'class' : 'row cols-edge prods_item-card'})

    for div in productDivs:
        url= div.find('a')['href']
        URL= "https://www.watchfinder.co.uk" + url
        URL = URL.replace(' ', '%20')
        print("Fetching Product: ", URL)
        try:
            urlpage=urlopen(URL).read()
        except:
            urlpage = None

        if(urlpage == None):
            print("Timeout Exception")
            continue
        urlpage=urlopen(URL).read()
        soup = BeautifulSoup(urlpage, "html.parser")
        

        for h1 in soup.find_all('h1', class_="col-md-5 prod_name"):
            product_title = h1.find_all('span')
            brand=  product_title[0].text
            name= product_title[1].text
            model=  product_title[1].text
            model_no= product_title[2].text

        metaTag= soup.find('div', class_ = "col-md-5 prod_id")
        url = metaTag.find("meta", itemprop="url")
        priceCurrency = metaTag.find("meta", itemprop= "priceCurrency")
        price = metaTag.find("meta", itemprop= "price")
        Product_url= url["content"]
        Currency= priceCurrency["content"]
        price=  price["content"] 

        retailPrice= soup.find('div', class_= "prod_price-info")
        try:
            retail_price= retailPrice.text
        except:
            retail_price= None

        divs = soup.findAll("table", {"class": "table prod_info-table"})
        for div in divs:
            row = ''
            rows = div.findAll('tr')
            for row in rows:
                if(row.text.find("Bracelet material") > -1):
                    bracelet_material= row.text
                    try:
                        band_color= bracelet_material.split('-')[1]
                    except:
                        band_color = None

                elif(row.text.find("Year") > -1):
                    year= row.text
                elif(row.text.find("Box") > -1):
                    box= row.text
                elif(row.text.find("Papers") > -1):
                    papers= row.text
                elif(row.text.find("Product code") > -1):
                    product_code= row.text
                elif(row.text.find("Movement") > -1):
                    movement= row.text
                elif(row.text.find("Case size") > -1):
                    case_size= row.text
                elif(row.text.find("Case material") > -1):
                    case_material= row.text
                elif(row.text.find("Dial type") > -1):
                    dial_type= row.text
                elif(row.text.find("Water resistance") > -1):
                    water_resistance= row.text


        table = soup.findAll('div',attrs={"class":"prod_desc row hidden-sm"})
        for x in table:
            product_detail= x.find('p').text


        divData=soup.find('div',{"id":"stock_gallery"})
        images = divData.find_all('img')
        for image in images:
            image_link= image['srcset']
            imgs = image_link.split(',', 1)[0]
            all_images= imgs.replace("data:image/gif;base64", " ")
            

        
        fetch_date= "2022-o5-08"


        conditionTag = soup.find_all('div', class_ = "menu-side-transition")[-1]
        condition= conditionTag.find("meta", itemprop="itemCondition")
        watch_condition= condition["content"] 

        # create a dictionary
        product = {}
        product['Product Url']= Product_url
        product['Brand']= brand
        product['Name']= name
        product['Model']= model
        product['Model No']= model_no
        product['Currency']= Currency
        product['Price']= price
        product['Final Price']= price
        product['Retail Price']= retail_price
        product['Band Color']= band_color
        product['Year']= year
        product['Box']= box
        product['Papers']= papers
        product['Product Code']= product_code
        product['Movement']= movement
        product['Case Size']= case_size
        product['Case Material']= case_material
        product['Bracelet Material']= bracelet_material
        product['Dial Type']= dial_type
        product['Water Resistance']= water_resistance
        product['Watch Details']= product_detail
        product['Watch images']= all_images
        product['Fetch Date']= fetch_date
        product['Condition']= watch_condition
        products.append(product)
        
    jsonstr= json.dumps(products)
    print('Saving File: ' + str(page_number))
    with open('/Users/poonamdhankher/Downloads/test/8orn Task/product_data'+ str(page_number) + '.json', 'w') as f:
        print(jsonstr, file=f)

    with open('/Users/poonamdhankher/Downloads/test/8orn Task/product_data'+ str(page_number) + '.json') as json_file:
        jsondata = json.load(json_file)
    
    data_file = open('/Users/poonamdhankher/Downloads/test/8orn Task/watches_data' + str(page_number) + '.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()

        


