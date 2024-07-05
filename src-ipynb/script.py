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
#nltk.download('stopwords')
#nltk.download('punkt')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

from IPython.display import Image
from IPython.core.display import HTML

### load the data
def parse(path):
    data = []
    with gzip.open(path) as f:
        for l in f:
            data.append(json.loads(l.strip()))
        return(data)

path_metaData_cellPhones = './meta_Cell_Phones_and_Accessories.json.gz'
data_metaData_cellPhones = parse(path_metaData_cellPhones)
df_metaData_raw_cellPhones = pd.DataFrame.from_dict(data_metaData_cellPhones)
df_metaData_raw_cellPhones.head(2)