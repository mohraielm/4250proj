# TfidfVectorizer
# CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd

# set of documents
train = ['The sky is blue.','The sun is bright.']
test = ['The sun in the sky is bright', 'We can see the shining sun, the bright sun.']

# instantiate the vectorizer object
countvectorizer = CountVectorizer(analyzer= 'word', stop_words='english')

# convert the training set into a matrix. This can be done in one step by using the function .fit_transform()
countvectorizer.fit(train)

# checking the index terms
print(countvectorizer.vocabulary_)

training_v = countvectorizer.transform(train)

#retrieve the terms found in the corpora
count_tokens = countvectorizer.get_feature_names_out()

# showing the training term matrix in an organized way by using a data frame
print("Count Vectorizer Training\n")
print(pd.DataFrame(data = training_v.toarray(),index = ['Doc1','Doc2'],columns = count_tokens))

# convert the test set into a matrix based on the training set index terms.
test_v  = countvectorizer.transform(test)

# showing the test term matrix in an organized way by using a data frame

print("Count Vectorizer Test\n")
print(pd.DataFrame(data = test_v.toarray(),index = ['Doc1','Doc2'],columns = count_tokens))

# Transfer the training term matrix of Countvectorizer to tf-idf by using TfidfTransformer

tfidf_training = TfidfTransformer()

tfidf_training.fit(training_v)
tfidf_training_matrix = tfidf_training.transform(training_v)

print("TFIDF transformer using Count Vectorizer Training\n")
print(pd.DataFrame(data = tfidf_training_matrix.toarray(),index = ['Doc1','Doc2'],columns = count_tokens))

tfidf_test = TfidfTransformer()

tfidf_test.fit(test_v)
tfidf_test_matrix = tfidf_test.transform(test_v)

print("TFIDF transformer using Count Vectorizer Test\n")
print(pd.DataFrame(data = tfidf_test_matrix.toarray(),index = ['Doc1','Doc2'],columns = count_tokens))

print("")
