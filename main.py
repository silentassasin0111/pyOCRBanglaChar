#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored

import argparse
import numpy as np 
from preprocessing.utils import Preprocessor 
from modelBuilder.models import DenseNet
from keras.callbacks import ModelCheckpoint
from sklearn import metrics
import os

parser = argparse.ArgumentParser(description='Bangla OCR 50 class Alphabet DenseNet Model')
parser.add_argument("datafolder", help="/path/to/Data/Folder")
parser.add_argument("flag", help="Train/Test")

args = parser.parse_args()
database_path=args.datafolder
exec_flag=args.flag



def preProcess(database_path):
    preprocObj=Preprocessor(database_path=database_path)
    data=preprocObj.preprocess_data()    
    return data

def trainModel(data,epochs=250,batch_size=100,optimizer_func='rmsprop'):
    
    modelObj=DenseNet(compression=0.5,add_bottleneck=True,num_of_layers=12,dropout_rate=0.2)
    modelObj.buildDenseNet()

    model=modelObj.DenseNetModel

    model_name=modelObj.model_name+'optimizer:{}.hdf5'.format(optimizer_func)

    print(colored('Training model:{}'.format(model_name),'red'))
    
    model.summary()

    model.compile(optimizer=optimizer_func, loss='categorical_crossentropy', metrics=['accuracy'])
    epochs = epochs
    batch_size = batch_size
    
    checkpoint = ModelCheckpoint(filepath='saved_models/{}'.format(model_name), verbose=1, save_best_only=True)
    
    train_tensors=data[0]
    train_classes=data[1]
    
    validation_tensors=data[2]
    validation_classes=data[3]
    
    model.fit(train_tensors, train_classes,validation_data=(validation_tensors, validation_classes),epochs=epochs, batch_size=batch_size, callbacks=[checkpoint], verbose=1)


    
if __name__ == "__main__":
    if exec_flag=='Train':
        data=preProcess(database_path)    
        trainModel(data)

    elif exec_flag=='Test':
        print("Removed For Now!!!")

    else:
        print(colored('FLAG ERROR!!!','red'))    