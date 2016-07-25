from ShipList import ShipList
from ShipOrigin import ShipOrigin
from unicodedata import normalize
from threading import Thread, BoundedSemaphore

def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

pool = BoundedSemaphore()

class ShipProcessorThread(Thread):
    def __init__(self, cities, ships):

        Thread.__init__(self)

        self.cities = cities
        self.ships = ships
        self.threadName = "Thread-" + str(start) + "-" + str(end)
        self.resultSet = []

    def log(self, text):
        print "[" + self.threadName + "]" "-> " + text

    def setLista(self, lista):
        self.resultSet = lista

    def run(self):
        self.log("-> analyzing ships...")
        for ship in self.ships:
            self.log("analyzing..." + ship["id"])
            
            v = ShipOrigin(ship["id"])
            origin = v.analyzeOrigin()

            if origin == None:
                continue
            origin = remover_acentos(origin.lower())

            if origin in self.cities:                
                self.log(origin)
                pool.acquire()
                try:
                    self.resultSet.append(ship)
                finally:
                    pool.release()
