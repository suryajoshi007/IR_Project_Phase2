import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
from typing import List, Dict
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def _get_doc_id(self, doc):
        """ 
        Splits each line of the document, into doc_id & text.
        """
        arr = doc.split("\t")
        print(arr)
        return int(arr[0]), arr[1]

    def tokenizer(self, doc: str):
        """
        preprocessing text
        """
        
        docId, doctext = self._get_doc_id(doc)

        # lowercase text 
        doctext = doctext.lower()

        # retain only alphanumeric characters and whitespace
        doctext = re.sub(r'[^a-zA-Z0-9\s]', ' ', doctext)

        # remove excessive white spaces
        tokens =[token for token in doctext.split() if token]

        # remove stopwords and use porter stemmer on each token
        tokens = [
            self.ps.stem(token)
            for token in tokens
            if token and token not in self.stop_words
        ]


        # total token count after preprocessing
        total_token_count = len(tokens)

        token_dict = {}

        for token in tokens:
            token_dict[token] = token_dict.get(token, 0) + 1

        # calculate tf for each term
        for token in token_dict:
            token_dict[token] = token_dict[token] / total_token_count

        return docId, token_dict

    def calculate_tf_idf(self):
        pass



