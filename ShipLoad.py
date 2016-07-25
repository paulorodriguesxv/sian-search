from ShipProcessorThread import *
import json

class ShipLoad(object):
    def __init__(self, start, tam):
        self.startNo = start
        self.tamNo = tam
        self.threadName = "Thread-" + str(start)

    def log(self, text):
        print "[" + self.threadName + "]" "-> " + text

    def run(self):
        shiplist = ShipList(self.startNo, self.tamNo)

        self.log("Retrieving ships...")
        ships = shiplist.getList()

        outputFile = open(self.threadName + ".ships", 'w')
        try:
            json.dump(ships, outputFile)
        finally:
            outputFile.close()