import nltk
import os
path = os.path.join(os.path.dirname(__file__),"/nltk_data")
nltk.download('stopwords', download_dir=path)
