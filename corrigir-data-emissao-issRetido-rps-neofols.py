import xml.etree.ElementTree as ET
import logging
from os import walk

logger = logging.getLogger()
logger.propagate = True
counter = 0
serviceValue = ""
issValue = ""


def fixXML(xmlFile):

    with open("./erradas/" + xmlFile, encoding='utf-8') as file:

        tree = ET.parse(file)
        root = tree.getroot()

        for rps in root:  # root = <NeoGrid>
            for child in rps:
                if (child.tag == "servico"):
                    for value in child:
                        if (value.tag == "vlServicos"):
                            global serviceValue
                            serviceValue = value.text

                        if(value.tag == "vlDeducoes"):
                            if(value.text != "0.00"):
                                value.text = "0.00"

                        if(value.tag == "issRet"):
                            value.text = "2"

                        if(value.tag == "vlISS"):
                            global issValue
                            issValue = value.text

                        if(value.tag == "vlISSRet"):
                            value.text = "0.000"

                        if(value.tag == "baseCalculo"):
                            value.text = float(serviceValue) + float(issValue)

                        if(value.tag == "vliquiNFSe"):
                            value.text = serviceValue

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
