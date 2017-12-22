
# coding: utf-8

# # Distribution of Friends

# In[1]:


from __future__ import print_function
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize


# In[32]:


data_dir = "./dataset"


# In[33]:


import json, os
users = []
with open(os.path.join(data_dir, 'user.json')) as f:
    for line in f:
        users.append(json.loads(line))
#print(users[1])
print("Read {count} users".format(count=len(users)))


# In[5]:


friend_counts = []
for user in users:
    friend_counts.append(len(user["friends"]))
print("Counted {count} friend relationships".format(count=sum(friend_counts)))


# In[48]:


name = []
maxf = 1
with open(os.path.join(data_dir, 'review.json')) as f:
    for line in f:
        if json.loads(line)['user_id'] == "9iUkIqYh84eAOXBh-NPheA":
            name.append(json.loads(line))

df = pd.DataFrame(name)
df.to_csv('./Gary.csv', index=False)


# In[6]:


print("Fraction of users with no defined friends: %0.3f" % 
      (len([c for c in friend_counts if c==0]) / float(len(friend_counts))))


# In[7]:


nonzero_friend_counts = [c for c in friend_counts if c>0]


# In[8]:


def summary(data):
    print("n    = {n}\n"
          "mean = {mean}\n"
          "sd   = {sd}\n"
          "min  = {min}\n"
          "10%  = {p10}\n"
          "25%  = {p25}\n"
          "50%  = {p50}\n"
          "75%  = {p75}\n"
          "90%  = {p90}\n"
          "max  = {max}".format(
            n=len(data),
            min=min(data),
            p10=np.percentile(data, 10),
            p25=np.percentile(data, 25),
            p50=np.percentile(data, 50),
            p75=np.percentile(data, 75),
            p90=np.percentile(data, 90),
            mean=np.mean(data),
            sd=np.std(data),
            max=max(data)))
summary(nonzero_friend_counts)


# In[9]:


def powerlaw(p, x):
    return p[0] * (x**p[1])

def fitfunc(p,x):
    return p[0] + p[1] * x 

def errfunc(p, x, y):
    return (y - fitfunc(p, x))/ (fitfunc(p, x)+1)

def fit_to_powerlaw(xs,ys):
    logx = np.log10(np.maximum(np.ones(len(xs)),xs))
    logy = np.log10(np.maximum(np.ones(len(ys)),ys))
    pinit = [max(ys), -1.0]
    out = optimize.leastsq(errfunc, pinit, args=(logx, logy), full_output=1)
    pfinal = out[0]
    index = pfinal[1]
    amp = 10.0**pfinal[0]
    return (amp, index)


# In[10]:


y, bins, patches = plt.hist(nonzero_friend_counts, 12, log=True, facecolor='#6699cc', alpha=0.45)

p = fit_to_powerlaw(bins[:-1], y)
print("p=",p)
plt.plot(bins, powerlaw(p, bins), 'g--', lw=2)

plt.xlabel('Friends')
plt.title('Histogram of number of friends')
plt.grid(True)
plt.show()


# # Distribution of Reviews per user

# In[41]:


reviews = []
with open(os.path.join(data_dir, 'review.json')) as f:
    for line in f:
        reviews.append(json.loads(line))
print("Read {count} reviews".format(count=len(reviews)))


# In[14]:


user_review_count = {}
for review in reviews:
    user_id = review["user_id"]
    if user_id in user_review_count:
        user_review_count[user_id] += 1
    else:
        user_review_count[user_id] = 1
#summary(user_review_count.values())


# In[15]:


summary([user['review_count'] for user in users])


# In[16]:


sum([user['review_count'] for user in users])


# In[17]:


sum(user_review_count.values())


# In[18]:


len([user['user_id'] for user in users if user_review_count[user['user_id']] > user['review_count']])


# In[19]:


review_counts = [user['review_count'] for user in users if user['review_count']>0 and user['review_count']<100]
y, bins, patches = plt.hist(review_counts, 16, log=True, facecolor='#6699cc', alpha=0.45)

p = fit_to_powerlaw(bins[:-1], y)
print("p=",p)
plt.plot(bins, powerlaw(p, bins), 'g--', lw=2)

plt.xlabel('Count of reviews')
plt.ylabel('Users')
plt.title('Histogram of number of reviews')
plt.grid(True)
plt.axis([0, 100, 0, 250000])
plt.show()


# In[20]:


len([user['review_count'] for user in users if user['review_count']>100])


# # Ratings

# In[ ]:


People seem to review things they like. The distribution of ratings is heavily skewed towards 4 and 5 stars.


# In[25]:


average_stars = [user['average_stars'] for user in users]
y, bins, patches = plt.hist(average_stars, 5, facecolor='#6699cc', alpha=0.45)

plt.xlabel('average stars given')
plt.ylabel('users')
plt.title('Histogram of average ratings')
plt.grid(True)
#plt.axis([0, 5, 0, 250000])
plt.show()

