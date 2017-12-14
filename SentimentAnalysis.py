from collections import Counter
import numpy as np
#Ejemplos de algoritmos que pueden probar (pueden usar otros si desean)
from sklearn.model_selection import cross_val_score
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier


#Archivo con contenido de reviews de películas
g = open('reviews.txt','r')
reviews = list(map(lambda x:x[:-1],g.readlines()))
g.close()

#Archivo con las etiquetas (POSITIVE,NEGATIVE)
g = open('labels.txt','r')
labels = list(map(lambda x:x[:-1].upper(),g.readlines()))
g.close()

# Se transforma todas las etiquetas a valores numéricos (1,0)
label2index = {}
for i, label in enumerate(list(set([x for x in labels]))):
    label2index[label] = i

y = np.array([label2index[x] for x in labels])
y.shape

positive_counts = Counter()
negative_counts = Counter()
total_counts = Counter()

for review, label in zip(reviews, labels):
    if label == 'POSITIVE':
        positive_counts.update(set(review.split(" ")))
    else:
        negative_counts.update(set(review.split(" ")))
total_counts.update(positive_counts)
total_counts.update(negative_counts)

frequency_cutoff = 50
pos_neg_ratios = Counter()
for term, cnt in list(total_counts.most_common()):
    if cnt >= frequency_cutoff: # common words only
        pos_neg_ratios[term] = np.log((positive_counts[term]+0.0001) / \
                                      (negative_counts[term]+1))

polarity_cutoff = 1.5
review_vocab = [x for x in pos_neg_ratios.keys() \
                if pos_neg_ratios[x] >= polarity_cutoff or \
                   pos_neg_ratios[x] <= -polarity_cutoff]

from sklearn.feature_extraction.text import TfidfVectorizer
X = TfidfVectorizer(vocabulary=review_vocab).fit_transform(reviews)

def run_model(clf, X, y):
    scores = cross_val_score(clf, X, y, cv=5)
    print("%s accuracy: %0.2f (+/- %0.2f)" % \
          (str(clf.__class__).split('.')[-1].replace('>','').replace("'",''),
          scores.mean(), scores.std() * 2))

def run_models(X, y):
    run_model(LinearSVC(), X, y)
    run_model(SGDClassifier(), X, y)
    run_model(Perceptron(), X, y)
    run_model(PassiveAggressiveClassifier(), X, y)
    run_model(BernoulliNB(), X, y)
    run_model(MultinomialNB(), X, y)
    #run_model(KNeighborsClassifier(), X, y)
    #run_model(NearestCentroid(), X, y)
    #run_model(RandomForestClassifier(n_estimators=100, max_depth=10), X, y)

run_models(X, y)