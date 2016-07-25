
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

class ShipList(object):
    
    def __init__(self, lista, initQuantReg=0, quantReg=500):
        self.apiroot = "http://www.an.gov.br/sian/multinivel/Multinivel_Consulta4.asp"

        self.payload= dict(  v_ini=initQuantReg,
                        v_intQuantReg=quantReg,
                        v_intTotalReg=48895,
                        v_codReferenciaPai_id=567717,
                        v_codFundo_ID=1462,
                        v_pula_nivel=1,
                        v_exibe_associa=1,
                        v_NroOrdemInicial="",
                        v_titulo=""
        )
    
    def getList(self):
        resultSet = []

        r = requests.get(self.apiroot, params=self.payload)

        body = r.text.encode("utf-8")
        body = body.replace("</td></td>", "<td>")


        #html.parser
        #html5lib
        #lxml
        soup = BeautifulSoup(body, 'lxml')

        ship_table = soup.find('table', {'class': 'tabelabordatotal'})

        #lista = []
        bCabecalho = True

        for ship in ship_table.find_all_next('tr'):
            try:
                if bCabecalho:
                    bCabecalho = False
                    continue 
                
                lista = []
                i=0
                for td in ship.find_all('td'):
                    try:
                        i += 1;

                        if (i in [2]):
                            text = td.a["href"]
                            text = text.partition('(')[-1].rpartition(')')[0]
                            lista.append(text)

                        if (i in (5, 6, 7)):
                            text = td.get_text().encode("latin-1")
                            lista.append(text)
                    except:
                        self.log("Oops!",sys.exc_info()[0],"occured.")
                
                resultData = dict(id=lista[0],
                                    title=lista[1].replace("\n", ""),
                                    refid=lista[2].replace("\n", ""),
                                    refdate=lista[3].replace("\n", ""))
                resultSet.append(resultData)
            except:
                self.log("Oops!",sys.exc_info()[0],"occured.")

        return resultSet    