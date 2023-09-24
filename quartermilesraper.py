import requests
import csv
from bs4 import BeautifulSoup
import re

#Creating the file header
fieldnames = ['Brand', 'Model', 'Generation', 'Spec-model', 'Acceleration 0-100 km/h', '1/4tb mile ET']
with open('qm.csv', 'w', newline='') as csvfile:
   writer = csv.writer(csvfile)
   writer.writerow(fieldnames)

#Lists
brandurls = []
modelurls = []
submodelurls = []
submodelurls_cleans = []
specmodelurls = []
cardata = []

#Brand URL collecting
topurl = 'https://www.auto-data.net/en/allbrands'
toppage = requests.get(topurl)
topsoup = BeautifulSoup(toppage.content, "html.parser")
#Comment out the bellow line if you just want to scrape one brand bellow 
#result_topurls = topsoup.body.find_all('a', href=re.compile('tesla'), class_='marki_blok')
#Comment the bellow line if you just want to scrape one brand above 
result_topurls = topsoup.body.find_all('a', class_='marki_blok')
for result_topurl in result_topurls:
    brandurl = 'https://www.auto-data.net' + result_topurl.get('href')
    brandurls.append(brandurl)

#Model URL collecting
for brandurl in brandurls:
    brandpage = requests.get(brandurl)
    brandsoup = BeautifulSoup(brandpage.content, "html.parser")
    result_brandurls = brandsoup.body.find_all('a', class_='modeli')
    for result_brandurl in result_brandurls:
        modelurl = 'https://www.auto-data.net' + result_brandurl.get('href')
        modelurls.append(modelurl)
        #print(modelurl)

#Sub-Model URL collecting
for modelurl in modelurls:
    modelpage = requests.get(modelurl)
    modelsoup = BeautifulSoup(modelpage.content, "html.parser")
    result_modelurls = modelsoup.body.find_all('a', class_='position')
    for result_modelurl in result_modelurls:
        submodelurl = 'https://www.auto-data.net' + result_modelurl.get('href')
        submodelurls.append(submodelurl)
submodelurls_cleans = list(set(submodelurls))

#Spec-Model URL collecting, write the result in a file
fspecmodelurl = open('specmodelurl.txt', 'w')
for submodelurls_clean in submodelurls_cleans:
    specmodelpage = requests.get(submodelurls_clean)
    specmodelsoup = BeautifulSoup(specmodelpage.content, "html.parser")
    result_specmodelurls = specmodelsoup.body.find_all('a', href=re.compile('/en/'))
    for result_specmodelurl in result_specmodelurls:
        if re.search('Dimensions', str(result_specmodelurl)):
            specmodelurl = 'https://www.auto-data.net' + result_specmodelurl.get('href')
            fspecmodelurl.write(specmodelurl + '\n')
fspecmodelurl.close()

with open('specmodelurl.txt') as specmodelurl_file:
    while specmodelurl_line := specmodelurl_file.readline():
        specmodelurl=specmodelurl_line.rstrip()
        specmodelurls.append(specmodelurl)

#Scraping the Data
for specmodelurl in specmodelurls:
    specpage = requests.get(specmodelurl)
    soup = BeautifulSoup(specpage.content, "html.parser")
    result_headers = soup.body.find_all('th', string=re.compile('Brand|Model |Generation |Modification (Engine) |Acceleration 0 - 100 km/h'))
    for result_header in result_headers:
        cardata.append(result_header.next_sibling.text)
    weight_to_power_header = soup.body.find('th', string='Weight-to-power ratio ')
    try: 
        weight_to_power = round((5.825*(float(weight_to_power_header.next_sibling.text.split()[0])*2.204622)**0.33333),3)
    except AttributeError:
        weight_to_power = 'not known'
    else:
        weight_to_power = round((5.825*(float(weight_to_power_header.next_sibling.text.split()[0])*2.204622)**0.33333),3)
    cardata.append(weight_to_power)
    with open('qm.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(cardata)
    cardata = []

