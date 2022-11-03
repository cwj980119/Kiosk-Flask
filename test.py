import dlib,cv2
import numpy as np
from keras.models import load_model
import pymysql
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
import json
import sys
import tensorflow as tf
import keras


load_model = load_model('tl_20_cropped_e20_b200.h5')
load_model.summary()

load_model.fit(train_dataset, epochs=20)