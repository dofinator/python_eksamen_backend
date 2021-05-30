
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing


import sys

sys.path.insert(0, '/home/jovyan/python_eksamen_backend/src/utils')
from locate_near_zips import get_zips

sys.path.insert(0, "/home/jovyan/python_eksamen_backend/src/webscraping")
from user_input import make_df_from_input

data = [[2, 2900, 7, 246, 125, 7958, 2, 640 ]]
testing_frame = pd.DataFrame (data, columns = ['house_type','house_zip_code', 'house_rooms', 'house_square_meters',
       'house_year', 'house_taxes', 'house_energy', 'house_ground_area'])

def train_model (df_residence):
    df = pd.read_csv('/home/jovyan/python_eksamen_backend/data/residence.csv',sep=";", index_col=False)

    # Encode the house type from string to integer
    label_enc =preprocessing.LabelEncoder()
    df['house_type'] = label_enc.fit_transform(df['house_type'].astype(str))
    # Encode the house energy from string to integer
    df['house_energy'] = label_enc.fit_transform(df['house_energy'].astype(str))

    zip = int((df_residence[['house_zip_code']].at[0, 'house_zip_code']))

    zips = get_zips(zip)

    df = df.loc[df['house_zip_code'].isin(zips)]

    #Target
    df_y = df[['house_price']]

    #Data
    df_x = df[['house_type','house_zip_code', 'house_rooms', 'house_square_meters',
       'house_year', 'house_taxes', 'house_energy', 'house_ground_area']]

    reg = linear_model.LinearRegression()

    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.20, random_state=42)

    norm = MinMaxScaler().fit(x_train)

    x_train_norm = norm.transform(x_train)

    #x_test_norm = norm.transform(x_test)

    reg.fit(x_train_norm, y_train)

    df_residence_norm = norm.transform(df_residence)

    pred = reg.predict(df_residence_norm)

    print("Din forventede huspris er: ", pred)

train_model(make_df_from_input())