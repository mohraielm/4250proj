# TfidfVectorizer
# CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# set of documents
train = ['The sky is blue.','The sun is bright.']
test = ['The sun in the sky is bright', 'We can see the shining sun, the bright sun.']

# instantiate the vectorizer object
tfidfvectorizer  = TfidfVectorizer(analyzer= 'word', stop_words='english')

# convert the training set into a matrix. This can be done in one step by using the function .fit_transform()
tfidfvectorizer.fit(train)

# checking the index terms
print(tfidfvectorizer.vocabulary_)

training_v = tfidfvectorizer.transform(train)

#retrieve the terms found in the corpora
tfidf_tokens = tfidfvectorizer.get_feature_names_out()

# showing the term matrix in an organized way by using a data frame
print("TD-IDF Vectorizer Training\n")
print(pd.DataFrame(data = training_v.toarray(),index = ['Doc1','Doc2'],columns = tfidf_tokens))

# convert the test set into a matrix based on the training set index terms.
test_v  = tfidfvectorizer.transform(test)

# showing the term matrix in an organized way by using a data frame

print("TD-IDF Vectorizer Test\n")
print(pd.DataFrame(data = test_v.toarray(),index = ['Doc1','Doc2'],columns = tfidf_tokens))

print("")