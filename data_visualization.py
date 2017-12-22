import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords


yelp = pd.read_csv('/usr/local/Cellar/bigdatahw3/filtered_range_review.csv')

yelp['text length'] = yelp['text'].apply(len)
yelp.head()


sns.boxplot(x='stars', y='text length', data=yelp)
plt.show()