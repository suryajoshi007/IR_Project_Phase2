from collections import OrderedDict
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
from typing import List, Dict
from preprocessor import Preprocessor
from postinglist import PostingList
import math

nltk.download('stopwords')

class Indexer:


    def __init__(self, index_file = "./data/input_corpus.txt"):

        self.index_file = index_file
        self.index = {}
        self.preprocessor = Preprocessor()

    def build_index(self):

        print(f"Building Index from Input File: {self.index_file}")

        with open(self.index_file, 'r') as file:

            temp_index = [self.preprocessor.tokenizer(doc) for doc in file]
        
        # sort based on docIds
        temp_index.sort(key = lambda x: x[0])

        for docId, token_dict in temp_index:

            for token, tf in token_dict.items():

                if token not in self.index:
                    self.index[token] = PostingList()
                
                self.index[token].insert_end(docId, tf)

        total_doc_count = len(self.index.keys())

        """
            for each posting list:
                calculate idf = total no. of docs / len of posting list
                insert skip pointers
        """

        for posting_list in self.index.values():

            posting_list.insert_skip_pointers()

            posting_list.idf = total_doc_count / posting_list.length

            # posting_list.idf = math.log(total_doc_count / (posting_list.length + 1))

            posting_list.calculate_tf_idf()
    

    def get_index(self):
        return self.index
    
    def get_postinglists(self, queries):

        qterms = []
        for query in queries:
            _, tokens = self.preprocessor.tokenizer(f"0\t{query}")
            qterms.extend(tokens)

        qterms = set(qterms)

        d = {}

        for term in qterms:
            d[term] = self.index[term].get_docId()
        
        return {
            "postingsList": OrderedDict(
                sorted(d.items(), key=lambda x: x[0])
            )
        }
    

    def get_postinglistsskip(self, queries):

        qterms = []
        for query in queries:
            _, tokens = self.preprocessor.tokenizer(f"0\t{query}")
            qterms.extend(tokens)

        qterms = set(qterms)

        d = {}

        for term in qterms:
            d[term] = self.index[term].get_docId_skip()
        
        return {
            "postingsListSkip": OrderedDict(
                sorted(d.items(), key=lambda x: x[0])
            )
        }


        








            

                

        
        