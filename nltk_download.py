#Author Diego Salas
#Date 11/12/2017
import nltk
import os
path = os.path.join(os.path.dirname(__file__),"nltk-data")
nltk.download('stopwords', download_dir=path)
