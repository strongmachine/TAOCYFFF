# -*- coding: utf-8 -*-
"""taocyfff.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l-6OzlXwunkY_4KO5J20Zws-244EiEWX
"""

import tensorflow as tf
from keras import datasets, layers, models

def create_model():
    '''
    Define a CNN where input to the model must be a 96 by 96 pixel, greyscale, image

    Returns:
    -------
    model: A fully-connected output layer with 30 facial keypoints
    '''

    model = models.Sequential()
    model.add(layers.Conv2D(32, (5,5), activation='relu', input_shape=(96, 96, 1)))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.1))

    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.2))
    
    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(256, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())

    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(30))
    return model

def compile_model(model, optimizer, loss, metrics):
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

def train_model(model, X_train, y_train):
    return model.fit(X_train, y_train, epochs=100, batch_size=200, verbose=1, validation_split=0.2)

def save_model(model, fileName):
    model.save(fileName + '.h5')

def load_model(fileName):
    return models.load_model(fileName + '.h5')



# pd.read_csv('/content/gdrive/MyDrive/project4_data/cnn_model.py.csv')

import pandas as pd
import numpy as np
import cv2
from pandas.core.frame import DataFrame
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/gdrive')

training = pd.read_csv('/content/gdrive/My Drive/training.csv')

def prepare_data(df):
    '''
    Prepare data image and target variables for training

    Parameters:
    ------------------
    df: Training DataFrame

    Returns:
    -------------
    X: Image (Feature) column
    y: Target column (facial points)

    '''
    
    # Create numpy array for pixel values in image column that are seperated by space
    df['Image'] = df['Image'].apply(lambda x: np.fromstring(x, sep=' '))

    # Drop all rows that have missing values in them
    df = df.dropna()

    # Normalize the pixel values, scale values between 0 and 1
    X = np.vstack(df['Image'].values) / 255.
    X = X.astype(np.float32)

    # return each image as a 96 x 96 x 1
    X = X.reshape(-1, 96, 96, 1)

    # 30 columns
    y = df[df.columns[:-1]].values

    # Normalize the target value, scale values between 0 and 1
    y = (y - 48) / 48

    # schuffle train data
    X, y = shuffle(X,y, random_state=42)
    y = y.astype(np.float32)

    return X,y

def plot_data(img, face_points):

    '''
    Plot image and facial keypoints

    Parameters:
    ----------------
    img: Image column value
    face_point: Target column value
    '''
    
    fig = plt.figure(figsize=(30,30))
    ax = fig.add_subplot(121)
    
    # Plot the image
    ax.imshow(np.squeeze(img), cmap='gray')
    face_points = face_points * 48 + 48

    # Plot the keypoints
    ax.scatter(face_points[0::2], face_points[1::2], marker='o', c='c', s=10)
    plt.show()

from google.colab import drive
drive.mount('/content/gdrive')

# Load training data
df = pd.read_csv('/content/gdrive/My Drive/training.csv')

X_train, y_train = prepare_data(df)

# Plot image and facial points for train dataset
plot_data(X_train[200], y_train[200])

# Create the model architecture
my_model = create_model()

# Compile the model with an appropriate optimizer and loss and metrics
compile_model(my_model, optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])

# Train the model
hist = train_model(my_model, X_train, y_train)

# Save the model
save_model(my_model, 'models/mm')






