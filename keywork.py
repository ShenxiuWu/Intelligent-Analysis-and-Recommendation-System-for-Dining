

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np

yelp_file = '/usr/local/Cellar/bigdatahw3/filtered_range_review.csv'

if not os.path.isfile(yelp_file):
    print(yelp_file, ' is missing.')
    exit()

# 1. Loading dataset
yelp_df = pd.read_csv(yelp_file, sep=',', usecols=['stars', 'text'])
yelp_df = yelp_df.loc[(yelp_df.stars == 5) | (yelp_df.stars == 1), :]
yelp_df.stars_map = yelp_df.stars.map({5: 1, 1: 0})

# 2. Feature matrix (X), response vector (y) and train_test_split
X = yelp_df.text
y = yelp_df.stars_map


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=5, shuffle=True)


# 3. Vectorize dataset
vect = CountVectorizer()
X_train_dtm = vect.fit_transform(X_train)
X_test_dtm = vect.transform(X_test)


# 4. Building and evaluating model
def build_evaluate_model(model_obj):
    print('-'*50)
    model_name = model_obj.__class__.__name__

    model_obj.fit(X_train_dtm, y_train)

    y_predict = model_obj.predict(X_test_dtm)
    print('\n', 'Accuracy of ', model_name, ' - ', metrics.accuracy_score(np.array(y_test), y_predict))
    print('\n', 'Confusion matrix \n', metrics.confusion_matrix(y_test, y_predict), '\n')

    y_predict_prob = model_obj.predict_proba(X_test_dtm)[:, 1]
    print('\n', 'Area Under Curve of ', model_name, ' - ', metrics.roc_auc_score(y_test, y_predict_prob), '\n\n')
    print('-' * 50)


nb = MultinomialNB()
build_evaluate_model(nb)

log_reg = LogisticRegression()
build_evaluate_model(log_reg)


# 5. Model insights
print('\n', 'Finding top rating and non-rating words')
X_train_tokens = vect.get_feature_names()

print('\n', 'Total Features: ', len(X_train_tokens))

one_star_token_count = nb.feature_count_[0, :]
five_star_token_count = nb.feature_count_[1, :]
token_count = pd.DataFrame({'token': X_train_tokens, 'one_star': one_star_token_count,
                            'five_star': five_star_token_count}).set_index('token')
token_count.one_star += 1
token_count.five_star += 1

print('\n', 'Total observations in each class ', nb.class_count_)
token_count.one_star_freq = token_count.one_star / nb.class_count_[0]
token_count.five_star_freq = token_count.five_star / nb.class_count_[1]

token_count['five_star_ratio'] = token_count.five_star_freq/ token_count.one_star_freq
token_count.sort_values('five_star_ratio', ascending=False, inplace=True)

print('\n', '-'*20, 'Top 20 five star rating words', '-'*20)
print(token_count.head(20))

print('\n', '-'*20, 'Top 20 one star rating words', '-'*20)
token_count.sort_values('five_star_ratio', ascending=True, inplace=True)
print(token_count.head(20))


