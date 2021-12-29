import xml.etree.ElementTree as ET
import logging
from os import walk

logger = logging.getLogger()
logger.propogate = True


def fixXML(xmlFile):

    with open("./erradas/" + xmlFile, encoding='latin-1') as file:

        tree = ET.parse(file)
        root = tree.getroot()
        iss = 0.03
        issRet = False
        vlISSRet = 0

        for child in root:
            for itens in child:
                if itens.tag == "servico":
                    for value in itens:
                        if value.tag == "alISS":
                            iss = round(float(value.text) / 100, 2)
                            logger.error(str(iss))

                        if value.tag == "vlServicos":
                            serviceValue = float(value.text)
                            roundedISS = str(round(serviceValue * iss, 2))

                            if len(roundedISS) == 3:
                                roundedISS += "00"
                            elif len(roundedISS) == 4 or len(roundedISS) == 5:
                                roundedISS += "0"

                        if value.tag == "issRet":
                            if value.text == "1":
                                issRet = True
                                vlISSRet = round(
                                    float(roundedISS) + round(float(roundedISS) * iss, 2), 2)

                        if value.tag == "vlISS":
                            value.text = value.text.replace(
                                value.text, roundedISS)

                        if value.tag == "vlISSRet" and issRet:
                            value.text = value.text.replace(
                                value.text, str(vlISSRet))

                        if value.tag == "vliquiNFSe":
                            if issRet:
                                value.text = value.text.replace(
                                    value.text, str(round(serviceValue - vlISSRet, 2)))
                            else:
                                value.text = str(serviceValue)

            output_file = xmlFile.replace(".xml", "") + "_CORRIGIDA.xml"

            with open("./corrigidas/" + output_file, 'w') as f:
                tree.write(f, encoding='unicode')


files = []
path = './erradas'

for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break

for rps in files:
    fixXML(rps)
