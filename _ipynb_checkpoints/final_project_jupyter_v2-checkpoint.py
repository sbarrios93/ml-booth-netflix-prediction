# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# https://medium.com/@tomar.ankur287/user-user-collaborative-filtering-recommender-system-51f568489727

import pandas as pd
import numpy as np
import math

Ratings = pd.read_csv('data/parsed_combined_data_1.txt')


# -

Ratings.columns = ['movieId', 'userId', 'rating', 'timestamp']

Ratings

Mean= Ratings.groupby(['userId'], as_index = False, sort = False).mean().rename(columns = {'rating': 'rating_mean'})[['userId','rating_mean']]
Ratings = pd.merge(Ratings,Mean,on = 'userId', how = 'left', sort = False)
Ratings['rating_adjusted']=Ratings['rating']-Ratings['rating_mean']
Ratings


distinct_movie = np.unique(Ratings['movieId'])
distinct_users = np.unique(Ratings['userId'])


def get_movie_rating(movie_id, user_id):
    user_data_append=pd.DataFrame()
    user_data_all=pd.DataFrame()

    user1_data =  Ratings[Ratings['userId']==user_id]
    user1_mean = user1_data["rating"].mean()
    user1_data = user1_data.rename(columns={'rating_adjusted':'rating_adjusted1'})
    user1_data = user1_data.rename(columns={'userId':'userId1'})
    user1_val = np.sqrt(np.sum(np.square(user1_data['rating_adjusted1']), axis=0))

    movie = movie_id

    item_user =  Ratings[Ratings['movieId']==movie]

    distinct_users1 = np.unique(item_user['userId'])


    j = 1
    
    print('distinct_users1: ' + str(len(distinct_users1)))

    for user2 in distinct_users1:
        user2_data = Ratings[Ratings['userId']==user2]
        user2_data = user2_data.rename(columns={'rating_adjusted':'rating_adjusted2'})
        user2_data = user2_data.rename(columns={'userId':'userId2'})
        user2_val = np.sqrt(np.sum(np.square(user2_data['rating_adjusted2']), axis=0))

        user_data = pd.merge(user1_data,user2_data[['rating_adjusted2','movieId','userId2']],on = 'movieId', how = 'inner', sort = False)
        user_data['vector_product'] = (user_data['rating_adjusted1']*user_data['rating_adjusted2'])

        user_data = user_data.groupby(['userId1','userId2'], as_index = False, sort = False).sum()

        user_data['dot'] = user_data['vector_product']/(user1_val*user2_val)

        user_data_all = pd.concat([user_data_all, user_data], ignore_index=True)

        j = j + 1 
        if j % 100 == 0:
            print('user_comparison: ' + str(j))
    
    print('user comparison done')
    user_data_all =  user_data_all[user_data_all['dot']<1]
    user_data_all = user_data_all.sort_values(['dot'], ascending=False)
    user_data_all = user_data_all.head(30)
    user_data_all['movieId'] = movie
    user_data_append = pd.concat([user_data_append, user_data_all], ignore_index=True)
 
    
    User_dot_adj_rating_all = pd.DataFrame()

    user_data_append_movie = user_data_append[user_data_append['movieId']==movie]
    User_dot_adj_rating = pd.merge(Ratings,user_data_append_movie[['dot','userId2','userId1']], how = 'inner',left_on='userId', right_on='userId2', sort = False)

    User_dot_adj_rating1 = User_dot_adj_rating[User_dot_adj_rating['movieId']==movie]

    if len(np.unique(User_dot_adj_rating1['userId'])) >= 2:

        User_dot_adj_rating1['wt_rating'] = User_dot_adj_rating1['dot']*User_dot_adj_rating1['rating_adjusted']

        User_dot_adj_rating1['dot_abs'] = User_dot_adj_rating1['dot'].abs()
        User_dot_adj_rating1 = User_dot_adj_rating1.groupby(['userId1'], as_index = False, sort = False).sum()[['userId1','wt_rating','dot_abs']]
        User_dot_adj_rating1['Rating'] = (User_dot_adj_rating1['wt_rating']/User_dot_adj_rating1['dot_abs'])+user1_mean
        User_dot_adj_rating1['movieId'] = movie
        User_dot_adj_rating1 = User_dot_adj_rating1.drop(['wt_rating', 'dot_abs'], axis=1)

        User_dot_adj_rating_all = pd.concat([User_dot_adj_rating_all, User_dot_adj_rating1], ignore_index=True)

    User_dot_adj_rating_all = User_dot_adj_rating_all.sort_values(['Rating'], ascending=False)
    return User_dot_adj_rating_all

# +
prediction = pd.DataFrame()
i = 0
with open('data/parsed_qualifying.txt', 'r') as f:
    for l in f.readlines():
        row = l.strip().split(',')
        print(row)
        user_movie_rating = get_movie_rating(movie_id=int(row[0]), user_id=int(row[1]))
        print(user_movie_rating)
        pd.concat([prediction, user_movie_rating])
        i = i + 1
        if i > 1:
            break

prediction
        
# -


