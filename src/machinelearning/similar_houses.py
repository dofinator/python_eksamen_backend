from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
from math import sqrt
import numpy as np


my_array = np.array([0.,0.78571429, 0.21428571, 0.11814346, 0.52422907, 0.03390525, 0.55555556, 0.00419759])

def get_similar_houses(user_input_house):
	
	df = pd.read_csv('/home/jovyan/python_eksamen_backend/data/residence.csv',sep=";", index_col=False)
	df_x = df[['house_type','house_zip_code', 'house_rooms', 'house_square_meters',
       'house_year', 'house_taxes', 'house_energy', 'house_ground_area']]
	df_y = df[['house_price']]
	df_x


	label_enc = preprocessing.LabelEncoder()
	df['house_type'] = label_enc.fit_transform(df['house_type'].astype(str))
	df['house_energy'] = label_enc.fit_transform(df['house_energy'].astype(str))
	df_x = df[['house_type','house_zip_code', 'house_rooms', 'house_square_meters',
       'house_year', 'house_taxes', 'house_energy', 'house_ground_area']]
	df_y = df[['house_price']]


	x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.20, random_state=0)
	norm = MinMaxScaler().fit(x_train)
	x_train_norm = norm.transform(x_train)
	x_test_norm = norm.transform(x_test)
	print(get_neighbors(x_test_norm, user_input_house, 5))

 
# calculate the Euclidean distance between two vectors
def euclidean_distance(row1, row2):
	distance = 0.0
	for i in range(len(row1)-1):
		distance += (row1[i] - row2[i])**2
	return sqrt(distance)
 
# Locate the most similar neighbors
def get_neighbors(train, user_input_house, num_neighbors):
	distances = list()
	for train_row in train:
		dist = euclidean_distance(user_input_house, train_row)
		distances.append((train_row, dist))
	distances.sort(key=lambda tup: tup[1])
	neighbors = list()
	for i in range(num_neighbors):
		neighbors.append(distances[i][0])
	return neighbors


get_similar_houses(my_array)