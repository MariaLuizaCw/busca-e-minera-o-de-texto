import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from xml.dom import minidom
from unidecode import unidecode
from numpy import dot
import sys
from numpy.linalg import norm
sys.path.insert(1, '../utils')
from read_config import read_config_file
from nltk.tokenize import RegexpTokenizer



class buscador():
    def __init__(self, input_path, results_path) -> None:
        self.inputs_path = input_path
        self.results_path = results_path
        self.config_dict = {}
        read_config_file(self.inputs_path + 'BUSCA.CFG', self.config_dict)
        print('Read Config File')
        print(self.config_dict)
    
    def search(self):
        results = pd.DataFrame()
        stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'[a-zA-Z]{3,}')
        vector_model= pd.read_csv(self.results_path + self.config_dict['MODELO'][0], sep=';', dtype={'doc':str})
        vector_model = vector_model.set_index('doc')
        consultas = pd.read_csv(self.results_path + self.config_dict['CONSULTAS'][0], sep=';', dtype={'QueryNumber':str})
        N = vector_model.shape[0]
        for index, row in consultas.iterrows():
            num_consulta = row['QueryNumber']
            consulta = row['QueryText']
            tokens = tokenizer.tokenize(consulta)
            if self.config_dict['USE'][0] == 'STEMMER':
                tokens = [stemmer.stem(t) for t in tokens]
            
            tf_idf_matrix = vector_model.loc[:, vector_model.columns.isin(tokens)]
            query_vector = np.ones(tf_idf_matrix.shape[1])
            
            
            matrix_norm = tf_idf_matrix.apply(lambda x: norm(x), axis=1)
            query_norm = norm(query_vector)
            query_docs_distance = 1 - (tf_idf_matrix@query_vector).divide(matrix_norm*query_norm).replace(np.nan, 0)
            
            
            query_docs_df = pd.DataFrame(query_docs_distance.sort_values(), columns=['distance']).reset_index()
            query_docs_df['ranking'] = [i+1 for i in range(0, N)]
            new_results = pd.concat([
                pd.Series([num_consulta for i in range(0, N)]), 
                query_docs_df.loc[:, ['ranking', 'doc', 'distance']].apply(lambda x: list(x), axis=1)
            ], axis=1)
            
            results = pd.concat([results, new_results])
        results = results.rename(columns={
            0: 'QueryNumber',
            1: 'Result'
        })
        results.to_csv(self.results_path + self.config_dict['RESULTADOS'][0], sep=';', index=None)