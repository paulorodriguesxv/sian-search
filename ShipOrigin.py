# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

class ShipOrigin(object):
    def __init__(self, codConfId):
        self.apiroot = "http://www.an.gov.br/sian/multinivel/Ver_Consulta_Dossie_Reduzida.asp"

        self.payload= dict( v_CodReferencia_ID=codConfId,
                            v_FlagBack="2",
                            v_CodRefPai_ID=""
                         )       

    def analyzeOrigin(self):
        resultSet = []

        r = requests.get(self.apiroot, params=self.payload)        

        body = r.text.encode("utf-8")
        soup = BeautifulSoup(body, 'lxml')

        ship_origin = soup.find_all('td', {'class': 'tdcadtxt'})

        bHeader = True
        for origin in ship_origin:            
            text = origin.get_text().encode("latin-1")
            
            if not ("Procedência" in text):
                continue

            if bHeader:
                bHeader = False
                continue

            text = origin.get_text().encode("latin-1")  
            return text.partition(':')[-1].strip()    
