# -*- coding: utf-8 -*-
"""highlight finder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tVg1UhT5eH0WZNNSTJeup9pvetQp_bvJ
"""

import cv2
from google.colab import drive
import numpy as np

drive.mount('/content/gdrive')

def highlight_finder(highlight_path, original_path):
  highlight_time = []
  h_video = cv2.VideoCapture(highlight_path)
  o_video = cv2.VideoCapture(original_path)
  h_fps = h_video.get(cv2.CAP_PROP_FPS)
  o_fps = o_video.get(cv2.CAP_PROP_FPS)
  retval, image = h_video.read()
  time = 0 
  h_count = 0
  o_count = 0

  while(h_video.isOpened()):
    retval, h_img = h_video.read()
    if not retval:
      break
    
    #h_img = Autoencoder(h_img)
    h_count += 1
    while(o_video.isOpened()):
      o_retval, o_img = o_video.read()
      if not o_retval:
        break
      #o_img = Autoencoder(o_img)
      o_count += 1
      if similarity(h_img, o_img, 1):
        if o_count//round(o_fps) not in highlight_time:
          highlight_time.append(o_count//round(o_fps))
        break
      
  h_video.release()
  o_video.release()
  return highlight_time

def similarity(h_img, o_img, threshold):
  h_img = np.array(h_img)
  o_img = np.array(o_img)
  return np.sum(np.abs(h_img-o_img)) / (h_img.shape[0] * h_img.shape[1]) < threshold

highlight_path = '/content/gdrive/My Drive/_-q1T2C3a0LvI.mp4'
original_path = '/content/gdrive/My Drive/_-q1T2C3a0LvI.mp4'

highlight_finder(highlight_path, original_path)
