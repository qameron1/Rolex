import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import re

urllib3.disable_warnings()

# List of each authorized dealer in the united stated 
def ads():
    data = pd.DataFrame()
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    name_table = soup.findAll('p', {"class" : "sc-pJhSf gdVGCp"})
    address_table = soup.findAll('address', {"class" : "sc-pZcYF Cqhcw"})
    data = data.append(name_table)
    data['Full_Address'] = address_table
    data.rename(columns={0:'Name'}, inplace=True)
    data.sort_values('Name', ascending=True, inplace=True)
# By region and location in the united states localities
    data['Full_Address'] = data['Full_Address'].apply(lambda x: x.text[:-13])
    data['Full_Address'] = data['Full_Address'].apply(lambda x: re.sub(r"(\w)([A-Z])", r"\1, \2", x))
    data['Full_Address'] = data['Full_Address'].str.split(',')
    data['Address'] = data['Full_Address'].str[0]
    data['City_State'] = data['Full_Address'].str[-1].str[:-5].str.strip()
    data.loc[data['City_State'].str.split(' ').str[-2].isin(['New', 'North', 'South', 'Rhode']), 'State'] \
        = data['City_State'].str.split(' ').str[-2:].str.join(',').str.replace(',', ' ')
    data.loc[~data['City_State'].str.split(' ').str[-2].isin(['New', 'North', 'South', 'Rhode']), 'State']  \
        = data['City_State'].str.split(' ').str[-1]
    data.loc[data['City_State'].str.split(' ').str[-1] == data['State'], 'City'] \
        = data['City_State'].str.split(' ').str[:-1].str.join(',').str.replace(',', ' ')
    data.loc[data['City_State'].str.split(' ').str[-1] != data['State'], 'City'] \
        = data['City_State'].str.split(' ').str[:-2].str.join(',').str.replace(',', ' ')
    data['Zip'] = data['Full_Address'].str[-1].str[-5:].str.strip()
    data.drop(['Full_Address', 'City_State'], axis=1, inplace=True)

    data['ID'] = (data.Name.str.replace(' ', '').str.upper() + data.Address.str.replace(' ','').str.upper()
        + data.State.str.replace(' ','').str.upper() + data.City.str.replace(' ', '').str.upper() + data.Zip)
    data = data[['Name', 'Address', 'City', 'State', 'Zip', 'ID']]
    data.to_csv(f'AD_List/Rolex_AD_List_{datetime.date.today().month}_{datetime.date.today().year}.csv', index=False)

# amount of rolex authorized dealers outstanding
def adcount():
    file = open('AD_Count/AD_Count.txt', 'a')
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    name_table = soup.findAll('p', {"class" : "sc-pJhSf gdVGCp"})
    address_table = soup.findAll('address', {"class" : "sc-pZcYF Cqhcw"})
    file.write('{}/{}: {} \n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    print('File Updated.')
    print('{}/{}: {} \r\n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    file.close()


if __name__ == "__main__":
    adcount()
    ads()
