from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import pandas as pd
import numpy as np
import gzip
import json
import os
import random
import re
import itertools
import glob
import string
from joblib import load
import pickle
import logging
import copy
import textstat

import matplotlib.pyplot as plt

import spacy
nlp_spacy = spacy.load("en_core_web_trf")

import nltk

from IPython.display import Image
from IPython.core.display import HTML

### load the data
def parse(path):
    data = []
    with gzip.open(path) as f:
        for l in f:
            data.append(json.loads(l.strip()))
        return(data)

path_metaData_cellPhones = './meta_Cell_Phones_and_Accessories.jsonl.gz'
data_metaData_cellPhones = parse(path_metaData_cellPhones)
df_metaData_raw_cellPhones = pd.DataFrame.from_dict(data_metaData_cellPhones)
df_metaData_raw_cellPhones.head(2)

path_review_cellPhones = './Cell_Phones_and_Accessories_5.json.gz'
data_review_raw_cellPhones = parse(path_review_cellPhones)
df_review_raw_cellPhones = pd.DataFrame.from_dict(data_review_raw_cellPhones)
df_review_raw_cellPhones.head(3)


cols = ["item", "user", "rating", "timestamp"]

path_rating_cellPhones = './Cell_Phones_and_Accessories.csv'
df_ratings_raw_cellPhones = pd.read_csv(path_rating_cellPhones, names = cols)

df_ratings_raw_cellPhones['timestamp'] = pd.to_datetime(df_ratings_raw_cellPhones['timestamp'],unit='s')



# Filter items with less than 6 categories & Split column of lists into multiple columns
df_metaData_raw_cellPhones_c1 = df_metaData_raw_cellPhones[df_metaData_raw_cellPhones.category.map(len) < 6 ]
df_categories_cellPhones = pd.DataFrame(df_metaData_raw_cellPhones_c1['category'].values.tolist()).add_prefix('category_')

df_metaData_concat_cellPhones = pd.concat([df_categories_cellPhones.reset_index(drop=True), df_metaData_raw_cellPhones_c1.reset_index(drop=True)], axis=1)

# Remove items without price
price_df_metaData_cellPhones = df_metaData_concat_cellPhones[df_metaData_concat_cellPhones.price != '']
# Remove items with wrong extracted price
price_df_metaData_cellPhones = price_df_metaData_cellPhones[price_df_metaData_cellPhones.price.str.len() < 9]
# Remove dollar ($) sign for sorting
price_df_metaData_cellPhones['price'] = price_df_metaData_cellPhones.price.str.replace('$', '').astype(float)

# Remove duplicates
subset = ['category_0', 'category_1', 'category_2', 'category_3', 'category_4', 'category', 'tech1', 'description', 'fit', 'title', 'also_buy', 'image',
       'tech2', 'brand', 'feature', 'rank', 'also_view', 'details', 'main_cat', 'date', 'price']

df_metaData_cellPhones = price_df_metaData_cellPhones.loc[price_df_metaData_cellPhones.astype(str).drop_duplicates(subset=subset, keep='first', inplace=False).index]
df_metaData_cellPhones.head(2)


