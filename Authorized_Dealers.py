import requests
import time
import urllib3
from bs4 import BeautifulSoup
import datetime

urllib3.disable_warnings()


def ads():
    starttime = time.time()
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    name_table = soup.findAll('p', {"class" : "sc-pRhbc ePDsLp"})
    address_table = soup.findAll('address', {"class" : "sc-oTzDS fotNMM"})
    # for x in address_table:
        # print(x.text)
    print('{}/{}: {}'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))

ads()