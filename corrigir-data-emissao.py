import xml.etree.ElementTree as ET
import logging
from os import walk
from datetime import datetime
import time

logger = logging.getLogger()
logger.propagate = True
counter = 0


def fixXML(xmlFile):

    with open("./erradas/" + xmlFile, encoding='utf-8') as file:

        tree = ET.parse(file)
        root = tree.getroot()

        for child in root:
            for itens in child:
                if itens.tag == "C":
                    for value in itens:
                        if value.tag == "DataEmissao":
                            dtnow = datetime.now()
                            day_string = dtnow.strftime("%Y-%m-%d")
                            hour_string = dtnow.strftime("%H:%M:%S")
                            value.text = day_string + "T" + hour_string
                            time.sleep(1)

            output_file = xmlFile.replace(".xml", "") + "_CORRIGIDA.xml"

            with open("./corrigidas/" + output_file, 'w') as f:
                tree.write(f, encoding='unicode')
            global counter
            counter += 1
            logger.error("{}. Arquivo {} corrigido com sucesso.".format(counter, output_file))


files = []
path = './erradas'

for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break

for rps in files:
    fixXML(rps)

wait = input("\nDigite 'Enter' para finalizar o script.")
