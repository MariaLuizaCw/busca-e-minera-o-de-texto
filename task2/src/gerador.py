import pandas as pd
import sys
from xml.dom import minidom
import numpy as np
from nltk.stem.porter import PorterStemmer
from unidecode import unidecode
sys.path.insert(1, '../utils')
from read_config import read_config_file
from nltk.tokenize import RegexpTokenizer

class gerador():
    def __init__(self, input_path, results_path) -> None:
        self.inputs_path = input_path
        self.results_path = results_path
        self.config_dict = {}
        read_config_file(self.inputs_path + 'GLI.CFG', self.config_dict)
        print('Read Config File')
        print(self.config_dict)
        
    def _parse_xml(self):
        records_data = []
        for xml_file in  self.config_dict['LEIA']:
            parsed_xml = minidom.parse(self.inputs_path + xml_file)
            records = parsed_xml.getElementsByTagName('RECORD')
            
            for record in records:
                recordnum = record.getElementsByTagName('RECORDNUM')[0].firstChild.nodeValue.strip()
                abstract = record.getElementsByTagName('ABSTRACT')
                extract = record.getElementsByTagName('EXTRACT')
                
                if len(abstract) > 0:
                    text = unidecode(abstract[0].firstChild.nodeValue.strip().lower())
                elif len(extract) > 0:
                    text = unidecode(extract[0].firstChild.nodeValue.strip().lower())
                else:
                    text = ''
                    
                records_data.append({'RECORDNUM': recordnum, 'TEXT': text})
        records_df = pd.DataFrame(records_data)
        return records_df
    def genereate_list(self):
        gli_dict = {}
        stemmer = PorterStemmer()
        records_df = self._parse_xml()
        for _, row in records_df.iterrows():
            text = row['TEXT']
            recordnum = row['RECORDNUM']
            tokenizer = RegexpTokenizer(r'[a-zA-Z]{3,}')
            words = tokenizer.tokenize(text)   
            if self.config_dict['USE'][0] == 'STEMMER':
                words = [stemmer.stem(w) for w in words]
            for w in words:
                if w in gli_dict:
                    gli_dict[w].append(recordnum)
                else:
                    gli_dict[w] = [recordnum]
        print('Generete List With ' + self.config_dict['USE'][0])
        glig_df = pd.DataFrame({'WORDS': gli_dict.keys(), 'RECORDS': gli_dict.values()})
        glig_df.to_csv(self.results_path+self.config_dict['ESCREVA'][0], index=False, sep=';')
        print(glig_df)