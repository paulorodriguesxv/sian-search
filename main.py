# -*- coding: utf-8 -*-
import threading
import json
import os.path

from ShipLoad import ShipLoad
from ShipProcessorThread import *

filename = "names.txt"
cities = [remover_acentos(line.strip().lower()) for line in open("names.txt", 'r')]

lista = []
threads = []

nindex = 0;
for threadI in xrange(0, 49):

    fname = "Thread-" + str(nindex) + ".ships"
    if os.path.isfile(fname):
        continue 
        
    sl = ShipLoad(nindex, 1000)
    sl.run()
    nindex += 1000

    
"""
sp1 = ShipProcessorThread(cities, nindex, nindex+1000)

    sp1.setLista(lista)
    sp1.start()

    threads.append(sp1)
    sp1.join()
# Wait for all threads to complete
for t in threads:
    t.join()

outfile = open('data.txt', 'w')
try:
    json.dump(lista, outfile)
finally:
    outfile.close()

print "Exiting Main Thread"
"""
