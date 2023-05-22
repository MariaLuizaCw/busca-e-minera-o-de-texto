from xml.dom import minidom
from unidecode import unidecode
import numpy as np
import sys
import pandas as pd
sys.path.insert(1, '../utils')
from read_config import read_config_file

class indexador():
    def __init__(self, input_path, results_path) -> None:
        self.inputs_path = input_path
        self.results_path = results_path
        self.config_dict = {}
        read_config_file(self.inputs_path + 'INDEX.CFG', self.config_dict)
        print('Read Config File')
        print(self.config_dict)
    def generete_tfidf_parameter(self):
        lista_df = pd.read_csv(self.results_path + self.config_dict['LEIA'][0], sep=';')
        freq_dict = {}
        word_doc_dict = {}
        docs_max_freq = {}
        for index, row in lista_df.iterrows():
            word = row['WORDS']
            records = eval(row['RECORDS'])
            
            word_doc_dict[word] = len(set(records))
            for doc in records:
                if doc in docs_max_freq:
                    docs_max_freq[doc] = max(docs_max_freq[doc], records.count(doc))
                else:
                    docs_max_freq[doc] = records.count(doc)
                freq_dict.setdefault(word, {})[doc] = records.count(doc)
        return freq_dict, word_doc_dict, docs_max_freq
    def tf_idf_default(self, word_doc_dict, freq_dict, docs_max_freq):
        words_list = word_doc_dict.keys()
        docs_list = docs_max_freq.keys()
        N = len(docs_list)
        tf_matrix = {}
        for doc in docs_list:
            for word in words_list:
                if doc in freq_dict[word]:
                    tf_matrix.setdefault(word, {})[doc] = (freq_dict[word][doc]/docs_max_freq[doc]) * np.log(N/word_doc_dict[word])
                else:
                    tf_matrix.setdefault(word, {})[doc] = 0 
        return tf_matrix
    
    def generate_model(self):
        freq_dict, word_doc_dict, docs_max_freq = self.generete_tfidf_parameter()
        tf_matrix = self.tf_idf_default(word_doc_dict, freq_dict, docs_max_freq)
        tf_matrix_df = pd.DataFrame(tf_matrix)
        tf_matrix_df = tf_matrix_df.reset_index(names=['doc'])
        print(tf_matrix_df.head())
        tf_matrix_df.to_csv(self.results_path + self.config_dict['ESCREVA'][0], sep=';', compression="gzip", index=False)