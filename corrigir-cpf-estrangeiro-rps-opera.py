from xml.dom.minidom import Element
import xml.etree.ElementTree as ET
import logging
from os import walk
from datetime import datetime
import time

logger = logging.getLogger()
logger.propagate = True
counter = 1
cpf = Element


def fixXML(xmlFile):

    with open("./erradas/" + xmlFile, encoding='utf-8') as file:

        tree = ET.parse(file)
        root = tree.getroot()

        for child in root:
            for itens in child:
                if itens.tag == "M":
                    for value in itens:
                        if value.tag == "Cpf":
                            global cpf
                            cpf = value
                        if value.tag == "TomadorEstrangeiro":
                            if value.text == "1":
                                cpf.tag = "Cnpj"
                                cpf.text = "99999999000000"

            output_file = xmlFile.replace(".xml", "") + "_CORRIGIDA.xml"

            with open("./corrigidas/" + output_file, 'w') as f:
                tree.write(f, encoding='unicode')
            global counter
            counter += 1
            logger.error("{}. Arquivo {} corrigido com sucesso.".format(
                counter, output_file))


files = []
path = './erradas'

for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break

for rps in files:
    fixXML(rps)

wait = input("\nDigite 'Enter' para finalizar o script.")
