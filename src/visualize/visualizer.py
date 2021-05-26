import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing



def plot_by_zip(zip):
    df = pd.read_csv('../data/residence.csv',sep=";", index_col=False)
    
    label_enc = preprocessing.LabelEncoder()
    
    # Encode the house type from string to integer
    df['house_type'] = label_enc.fit_transform(df['house_type'].astype(str))
    # Encode the house energy from string to integer
    df['house_energy'] = label_enc.fit_transform(df['house_energy'].astype(str))
    
    df = df.loc[df['house_zip_code'].isin([zip])]

    df.plot.scatter(x="house_square_meters", y="house_price");