from ShipList import ShipList
from ShipOrigin import ShipOrigin
from unicodedata import normalize
from threading import Thread, BoundedSemaphore
import json

def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

pool = BoundedSemaphore()

class ShipProcessorThread(Thread):
    def __init__(self, cities, filename):

        Thread.__init__(self)

        self.cities = cities
        
        with open(filename) as f:
            self.ships = json.loads(f.read())
            f.close()
        
        self.threadName = "Thread-" + filename 
        self.resultSet = []

    def log(self, text):
        print "[" + self.threadName + "]" "-> " + text

    def setLista(self, lista):
        self.resultSet = lista

    def run(self):
        self.log("-> analyzing ships...")
        for ship in self.ships:
            
            v = ShipOrigin(ship["id"])
            origin = v.analyzeOrigin()

            if origin == None:
                continue

            co = remover_acentos(origin.lower())
            co = co.replace("\r", ",")
            co = co.replace("escalas", "")
            co = co.replace("escala","")
            co = co.replace(":", "")
            co = co.replace(";", "")
            co = co.replace(" ", "")
            
            origins = co.split(',')

            for origin in origins:            
                if origin in self.cities:                
                    self.log("### " + origin + " ###" )
                    pool.acquire()
                    try:
                        self.resultSet.append(dict(ship=ship, origin=origin))
                    finally:
                        pool.release()
