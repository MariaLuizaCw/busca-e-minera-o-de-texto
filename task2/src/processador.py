from xml.dom import minidom
from unidecode import unidecode
import sys
import pandas as pd
sys.path.insert(1, '../utils')
from read_config import read_config_file

class processador():
    def __init__(self, input_path, results_path) -> None:
        self.inputs_path = input_path
        self.results_path = results_path
        self.config_dict = {}
        read_config_file(self.inputs_path + 'PC.CFG', self.config_dict)
        print('Read Config File')
        print(self.config_dict)
    def _parse_xml(self):
        print('Parsed XML')
        xml_file = self.inputs_path + self.config_dict['LEIA'][0]
        parsed_xml = minidom.parse(xml_file)
        return parsed_xml
    
    def _soma_string(self, score):
        digit_sum = 0
        for digit in score:
            digit_sum += int(digit)
        
        return digit_sum
    
    def generate_consultas(self):
        xml_data_queries = []
        query_elements = self._parse_xml().getElementsByTagName('QUERY')
        for query in query_elements:
            query_number = query.getElementsByTagName('QueryNumber')[0].firstChild.nodeValue
            query_text = query.getElementsByTagName('QueryText')[0].firstChild.nodeValue.strip()
            query_text = unidecode(query_text.replace(';', ' ')).lower()
            xml_data_queries.append([query_number, query_text])

        df_queries = pd.DataFrame(xml_data_queries, columns=['QueryNumber', 'QueryText'])

        df_queries.to_csv(self.results_path + self.config_dict['CONSULTAS'][0], index=False, sep=';')
        print('Generate Queries CSV')
        print(df_queries.head())
        
    def generate_esperados(self):
        xml_data_docs = []
        parsed_xml = self._parse_xml()
        for query in parsed_xml.getElementsByTagName('QUERY'):
            query_number = query.getElementsByTagName('QueryNumber')[0].firstChild.nodeValue
            for record in query.getElementsByTagName('Records')[0].getElementsByTagName('Item'):
                doc_number = record.firstChild.nodeValue
                doc_votes = self._soma_string(record.getAttribute('score'))
                
                xml_data_docs.append((query_number, doc_number, doc_votes))


        df_docs = pd.DataFrame(xml_data_docs, columns=['QueryNumber', 'DocNumber', 'DocVotes'])
        df_docs.to_csv(self.results_path + self.config_dict['ESPERADOS'][0], index=False, sep=';')
        
        print('Generate Queries CSV')
        print(df_docs.head())