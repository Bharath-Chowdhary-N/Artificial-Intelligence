# -*- coding: utf-8 -*-
"""CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j7XqcqWW2RoKNJQdYzSpFoxO_sr6rny8
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
class CNN():
  

  def __init__(self):
    self.load_train_and_validation_data()
    self.train()
  def load_train_and_validation_data(self):

    self.train_dir = os.path.join('Artificial-Intelligence//Direct Imaging//Images//Data//train')
    self.validation_dir = os.path.join('Artificial-Intelligence//Direct Imaging//Images//Data//validation')
    
    self.train_planet_dir = os.path.join(self.train_dir,'with_planet')  
    self.train_wo_planet_dir = os.path.join(self.train_dir,'without_planet') 
    self.validation_planet_dir = os.path.join(self.validation_dir,'with_planet')  
    self.validation_wo_planet_dir = os.path.join(self.validation_dir,'without_planet')  
    self.num_planet_tr = len(os.listdir(self.train_planet_dir))
    self.num_wo_planet_tr = len(os.listdir(self.train_wo_planet_dir))

    self.num_planet_val = len(os.listdir(self.validation_planet_dir))
    self.num_wo_planet_val = len(os.listdir(self.validation_wo_planet_dir))

    self.total_train = self.num_planet_tr + self.num_wo_planet_tr
    self.total_val = self.num_planet_val + self.num_wo_planet_val

    self.batch_size = 128
    self.epochs = 15
    self.IMG_HEIGHT = 150
    self.IMG_WIDTH = 150
  def train(self):   
  
    self.train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
    self.validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

    self.train_data_gen = self.train_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                           directory=self.train_dir,
                                                           shuffle=True,
                                                           target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                           class_mode='binary')
    self.val_data_gen = self.validation_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                              directory=self.validation_dir,
                                                              target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                              class_mode='binary')
    self.model_new = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', 
           input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH ,3)),
    MaxPooling2D(),
    Dropout(0.2),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(1)])
    
    self.model_new.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
    
    self.history = self.model_new.fit(
    self.train_data_gen,
    steps_per_epoch=self.total_train / self.batch_size,
    epochs=self.epochs,
    validation_data=self.val_data_gen,
    validation_steps=self.total_val / self.batch_size)