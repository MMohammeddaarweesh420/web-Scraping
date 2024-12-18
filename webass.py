import requests
from bs4 import BeautifulSoup
import csv 
import json
from itertools import zip_longest



#requests the url
result = requests.get("https://www.baraasallout.com/test.html")
src = result.content 
soup = BeautifulSoup(src, "lxml")
#print(soup)

#1:Extract Text Data: ()
Headline=[]
Pragraph=[]
Lestiteme=[]

headline= soup.find_all(name=["h1", "h2"] )
pragraph= soup.find_all("p")
list_elemnt= soup.find_all("li")

#save data from tags in list as text 
for i in range (len(headline)):
    Headline.append(headline[i].text)
"""
for i in range(len(headeing)):
    Headiing.append(headeing[i].text)"""

for i in range(len(pragraph)):
   Pragraph.append(pragraph[i].text) 
   
for i in range (len(list_elemnt)):
    Lestiteme.append(list_elemnt[i].text)


#save text data in csv file 
file_list =[Headline, Pragraph, Lestiteme] 
eported= zip_longest(*file_list)
with open(r'D:\python test\webass\Extract_text_data.csv', 'w', encoding='UTF8') as myfile:
    wr= csv.writer(myfile)
    wr.writerow(["Heading", "Paracraph", "ListItime"])
    wr.writerows(eported)




#2: Extract table data
table_data = []
table = soup.find('table')  # Adjust this if the table has a specific class or id
for row in table.find_all('tr')[1:]:  # Skip header row
    cols = row.find_all('td')
    product_name = cols[0].get_text(strip=True)
    price = cols[1].get_text(strip=True)
    stock_status = cols[2].get_text(strip=True)
    table_data.append([product_name, price, stock_status])

# Save to CSV
with open(r'D:\python test\webass\Extract_Table_Data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Stock Status'])
    writer.writerows(table_data)



#3: Extract Product Information (Cards Section)
product_info = []
cards = soup.find_all('div', class_='card')  
for card in cards:
    title = card.find('h3').get_text(strip=True)
    price = card.find('span', class_='price').get_text(strip=True)
    stock_availability = card.find('span', class_='availability').get_text(strip=True)
    button_text = card.find('button').get_text(strip=True)
    product_info.append({
        'title': title,
        'price': price,
        'stock_availability': stock_availability,
        'button_text': button_text
    })

# Save to JSON
with open(r'D:\python test\webass\Product_Information.json', 'w') as json_file:
    json.dump(product_info, json_file, indent=4)




#4: Extract Form Details
form_details = []
form = soup.find('form')  
for input_field in form.find_all('input'):
    field_name = input_field.get('name')
    input_type = input_field.get('type')
    default_value = input_field.get('value', '')
    form_details.append({
        'field_name': field_name,
        'input_type': input_type,
        'default_value': default_value
    })

# Save to JSON
with open(r'D:\python test\webass\Form_Details.json', 'w') as json_file:
    json.dump(form_details, json_file, indent=4)

#5:Extract Links and Multimedia:

links_data = []
for a in soup.find_all('a'):
    href = a.get('href')
    links_data.append({'link_text': a.get_text(strip=True), 'href': href})

# Extract video link from iframe
video_link = soup.find('iframe').get('src') if soup.find('iframe') else None

# Save to JSON
with open(r'D:\python test\webass\Links_and_Multimedia.json', 'w') as json_file:
    json.dump({'links': links_data, 'video_link': video_link}, json_file, indent=4)


#6:Scraping Challenge

featured_products = []
featured_section = soup.find('div', class_='featured-products')  # Adjust the class name as necessary
for product in featured_section.find_all('div', class_='product-card'):
    product_id = product.get('data-id')
    name = product.find('span', class_='name').get_text(strip=True)