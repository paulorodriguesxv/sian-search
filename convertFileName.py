import os
from shutil import copyfile
from pprint import pprint

files = os.listdir("pdf")

for item in files:
    day = item[:2]
    month = item[2:4]
    year = item[4:8]

    name = year + month + day

    copyfile("pdf/" + item, "cnv/" + name + "_" + item )

    print "Copiando... " + item
