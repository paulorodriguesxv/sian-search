import json
import datetime
import requests
import urlparse
from bs4 import BeautifulSoup
from pprint import pprint

def downloadFile(url, refdate):
    local_filename = "pdf/" + refdate + "_" + url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def parserPage(pageid, refdate):
    
    apiroot = "http://www.an.gov.br/sian/Multinivel/Lista_Diretorios.asp"
    payload = dict( visualiza=1,
                    v_CodReferencia_id=pageid)

    r = requests.get(apiroot, params=payload)
    body = r.text.encode("utf-8")
    body = body.replace("</td></td>", "<td>")


    soup = BeautifulSoup(body, 'lxml')
    ship_table = soup.find('a')
    ship_url = ship_table["href"]

    url_parsed = urlparse.urlparse(ship_url)
    pdf_url = urlparse.parse_qs(url_parsed.query)['v_arquivo'][0]

    downloadFile(pdf_url, refdate)

years_list = range(1875, 1901)

with open('data.json') as data_file:    
    data = json.load(data_file)

ships_sel = []

for item in data:
    refdate = item["ship"]["refdate"]
    try:
        year = datetime.datetime.strptime(refdate, "%d/%m/%Y").date().year

        if (year in years_list):
            ships_sel.append(item) 
    except:
        pass

for item in ships_sel:
    refid = item["ship"]["id"]
    refdate = item["ship"]["refdate"].replace("/", "")
    print refid

    parserPage(refid, refdate)
#pprint()
    