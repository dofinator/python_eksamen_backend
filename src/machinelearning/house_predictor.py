
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from termcolor import colored as cl

import sys
sys.path.insert(0, '/home/jovyan/python_eksamen/src/utils')
from locate_near_zips import get_zips


def predict_house_price(df_residence):
    # Encode the house_type from string to integer
    label_enc =preprocessing.LabelEncoder()
    df_residence['house_type'] = label_enc.fit_transform(df_residence['house_type'].astype(str))
    # Encode the house_energy from string to integer
    df_residence['house_energy'] = label_enc.fit_transform(df_residence['house_energy'].astype(str))


