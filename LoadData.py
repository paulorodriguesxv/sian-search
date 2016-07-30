import json
import datetime
from pprint import pprint

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

apiroot = "http://www.an.gov.br/sian/Multinivel/Imagem_Mapa.asp"
payload = dict( visualiza=1,
                v_CodReferencia_id=1012883)
