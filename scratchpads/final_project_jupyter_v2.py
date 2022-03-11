#!/usr/bin/env python
# coding: utf-8

# In[3]:


# https://medium.com/@tomar.ankur287/user-user-collaborative-filtering-recommender-system-51f568489727

import pandas as pd
import numpy as np
import math
import warnings

warnings.filterwarnings("ignore")
Ratings = pd.read_csv("data/parsed_combined_data_1.txt")


# In[4]:


Ratings.columns = ["movieId", "userId", "rating", "timestamp"]


# In[5]:


Ratings


# In[6]:


Mean = (
    Ratings.groupby(["userId"], as_index=False, sort=False)
    .mean()
    .rename(columns={"rating": "rating_mean"})[["userId", "rating_mean"]]
)
Ratings = pd.merge(Ratings, Mean, on="userId", how="left", sort=False)
Ratings["rating_adjusted"] = Ratings["rating"] - Ratings["rating_mean"]
Ratings


# In[7]:


distinct_movie = np.unique(Ratings["movieId"])
distinct_users = np.unique(Ratings["userId"])


# In[8]:


def get_movie_rating(movie_id, user_id):
    user_data_append = pd.DataFrame()

    user1_data = Ratings[Ratings["userId"] == user_id]
    user1_mean = user1_data["rating"].mean()
    user1_data = user1_data.rename(columns={"rating_adjusted": "rating_adjusted1"})
    user1_data = user1_data.rename(columns={"userId": "userId1"})
    user1_val = np.sqrt(np.sum(np.square(user1_data["rating_adjusted1"]), axis=0))

    movie = movie_id

    item_user = Ratings[Ratings["movieId"] == movie]

    distinct_users1 = np.unique(item_user["userId"])
    if len(distinct_users1) == 0:
        return pd.DataFrame([0])

    j = 1

    # print('distinct_users1: ' + str(len(distinct_users1)))

    # filter ratings for distinct users
    ratings_distinct_users = Ratings[Ratings["userId"].isin(distinct_users1)]

    rms_vals = ratings_distinct_users.groupby("userId").apply(
        lambda x: np.sqrt(np.sum(np.square(x["rating_adjusted"]), axis=0))
    )
    rms_vals.name = "rms_vals"

    ratings_distinct_users = ratings_distinct_users.merge(rms_vals, left_on="userId", right_index=True, how="left")

    ratings_distinct_users.rename(columns={"rating_adjusted": "rating_adjusted2"}, inplace=True)
    ratings_distinct_users.rename(columns={"userId": "userId2"}, inplace=True)

    user_data = pd.merge(user1_data, ratings_distinct_users, on="movieId", how="inner", sort=False)

    user_data["vector_product"] = user_data["rating_adjusted1"] * user_data["rating_adjusted2"]

    user_data_all = user_data.groupby(["userId1", "userId2", "rms_vals"]).sum().reset_index()

    user_data["dot"] = user_data["vector_product"] / (user1_val * user_data["rms_vals"])

    # print('user comparison done')
    user_data = user_data[user_data["dot"] < 1]
    user_data = user_data.sort_values(["dot"], ascending=False)
    user_data = user_data.head(30)
    user_data["movieId"] = movie
    user_data_append = pd.concat([user_data_append, user_data], ignore_index=True)

    User_dot_adj_rating_all = pd.DataFrame()

    user_data_append_movie = user_data_append[user_data_append["movieId"] == movie]
    User_dot_adj_rating = pd.merge(
        Ratings,
        user_data_append_movie[["dot", "userId2", "userId1"]],
        how="inner",
        left_on="userId",
        right_on="userId2",
        sort=False,
    )

    User_dot_adj_rating1 = User_dot_adj_rating[User_dot_adj_rating["movieId"] == movie]

    if len(np.unique(User_dot_adj_rating1["userId"])) >= 2:

        User_dot_adj_rating1["wt_rating"] = User_dot_adj_rating1["dot"] * User_dot_adj_rating1["rating_adjusted"]

        User_dot_adj_rating1["dot_abs"] = User_dot_adj_rating1["dot"].abs()
        User_dot_adj_rating1 = User_dot_adj_rating1.groupby(["userId1"], as_index=False, sort=False).sum()[
            ["userId1", "wt_rating", "dot_abs"]
        ]
        User_dot_adj_rating1["Rating"] = (
            User_dot_adj_rating1["wt_rating"] / User_dot_adj_rating1["dot_abs"]
        ) + user1_mean
        User_dot_adj_rating1["movieId"] = movie
        User_dot_adj_rating1 = User_dot_adj_rating1.drop(["wt_rating", "dot_abs"], axis=1)

        User_dot_adj_rating_all = pd.concat([User_dot_adj_rating_all, User_dot_adj_rating1], ignore_index=True)

        User_dot_adj_rating_all = User_dot_adj_rating_all.sort_values(["Rating"], ascending=False)
    return User_dot_adj_rating_all


# In[9]:


from tqdm import tqdm

prediction = pd.DataFrame()
i = 0
with open("data/parsed_qualifying.txt", "r") as f:
    for j, l in enumerate(tqdm(f.readlines())):
        row = l.strip().split(",")
        # print(row)
        user_movie_rating = get_movie_rating(movie_id=int(row[0]), user_id=int(row[1]))
        # print(user_movie_rating)
        pd.concat([prediction, user_movie_rating])
        i = i + 1
        if i > 100:
            break


# In[66]:


# In[63]:

# In[ ]:
