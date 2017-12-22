import math
import time
import pandas as pd
csvpath = '/usr/local/Cellar/2id_name.csv'
frame = pd.read_csv(csvpath)
ttuser = list(frame['user_id'])
#tuser = ttuser[0]
tuser = 'bLbSNkLggFnqwNNzzq-Ijw'

def calcuteSimilar(series1,series2):
    '''
    Cosine similarity calculation
    :data1: Series 1
    :data2: Series 2
    :return: similarity
    '''
    unionLen = len(set(series1) & set(series2))
    if unionLen == 0:
        return 0.0
    product = len(series1) * len(series2)
    similarity = unionLen / math.sqrt(product)
    return similarity

def calcuteUser(targetID=tuser,TopN=10):
    '''
    Compute the similarity between targetID users and other users
    :return:similarity TopN Series
    '''
    #frame = pd.read_csv(csvpath)                                                        #read & input data
    targetUser = frame[frame['user_id'] == targetID]['name']                          #the target user's data & info
    otherUsersID = [i for i in set(frame['user_id']) if i != targetID]                   #other users' ID
    otherUsers = [frame[frame['user_id'] == i]['name'] for i in otherUsersID]         #other users' data & info
    similarlist = [calcuteSimilar(targetUser, user) for user in otherUsers]              #Compute
    similarSeries = pd.Series(similarlist, index=otherUsersID)                           #Series
    return similarSeries.sort_values()[-TopN:]

def calcuteInterest(frame,similarSeries,targetItemID):
    '''
    Calculate the degree of interest of the target user to the target item
    :parameter: frame: data
    :parameter: similarSeries: The most similar K users in the whole target users
    :parameter: targetItemID: target item
    :return:Degree of interest
    '''
    similarUserID = similarSeries.index              #The K users who have the most similar interests with target user
    similarUsers = [frame[frame['user_id'] == i] for i in similarUserID]                 #The data of K users
    similarUserValues = similarSeries.values                 #Interest similarity between target users and other users
    UserInstItem = []
    for u in similarUsers:                                                     #Other users' interest in certain items
        if targetItemID in u['name'].values:
            UserInstItem.append(u[u['name'] == targetItemID]['stars'].values[0])
        else: UserInstItem.append(0)
    interest = sum([similarUserValues[v]*UserInstItem[v]/5 for v in range(len(similarUserValues))])
    return interest

def calcuteItem(targetUserID=tuser,TopN=10):
    '''
    Calculate the TopN items that are recommended to the users of targetUserID
    :parameter: csvpath: data path
    :parameter: targetUserID: target user
    :parameter: TopN:
    :return: TopN items and the degree of interest
    '''
    similarSeries = calcuteUser(targetID=targetUserID)                        #Calculate the most similar K users
    userMovieID = set(frame[frame['user_id'] == tuser]['name'])               #the item of target user interested in
    otherMovieID = set(frame[frame['user_id'] != tuser]['name'])              #the item of other users interested in
    movieID = list(userMovieID ^ otherMovieID)                                          #difference set
    interestList = [calcuteInterest(frame,similarSeries,movie) for movie in movieID]    #recommendation
    interestSeries = pd.Series(interestList, index=movieID)
    return interestSeries.sort_values()[-TopN:]                                         #TopN

if __name__ == '__main__':
    print('start..')
    start = time.time()
    a = calcuteItem()
    print(a)
    print('Cost time: %f'%(time.time()-start))