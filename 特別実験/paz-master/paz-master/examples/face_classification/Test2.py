import argparse
import cv2
import glob
import os
import time
from enum import Enum
import numpy as np
from PIL import Image
from matplotlib import pyplot
import csv
import pprint
import pandas as pd
from paz.pipelines import MiniXceptionFER
import JikkenModule


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Real-time face classifier')
    parser.add_argument('mode')
    
    args = parser.parse_args()
    MosaicMode=args.mode
    if(MosaicMode!="Upper" and MosaicMode!="Under" and MosaicMode!="In"):
        exit()

    test_data = open("C:/Users/chunn/Downloads/MTFL/training.txt", "r")

    # 行ごとにすべて読み込んでリストデータにする
    lines = test_data.readlines()
    test_data.close()
    
    
    data = pd.read_csv('C:/Users/chunn/Desktop/YNU/輪講/特別実験/fer2013.csv',delimiter=',',dtype='a')
    jikkenModuleUpper=JikkenModule.ImageClassifer(mosaicMode="Upper",maxMosaicRatio=30)
    #jikkenModuleUnder=JikkenModule.ImageClassifer(mosaicMode="Upper",maxMosaicRatio=30)
    #jikkenModule=JikkenModule.ImageClassifer(mosaicMode=MosaicMode,maxMosaicRatio=30)
    jikkenModuleAll=JikkenModule.ImageClassifer(mosaicMode="All",maxMosaicRatio=30)
    for i in range(0,len(data["emotion"])):
        # if i==0:
        #     jikkenModule.ShowResult("Fer2013")
        #     sys.exit(0)
        imagebuffer=np.array(data["pixels"][i].split())
        image=np.array([np.fromstring(image,np.uint8,sep=' ') for image in imagebuffer])
        image=image.reshape(48,48)
        image=cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        emotion=data["emotion"][i]
        totalNumberOfFiles=i
        correctEmotion=JikkenModule.ConvertEmotionToEnum(emotion)
        try:
            jikkenModuleUpper.AddImage(image,correctEmotion)
        except:
            pass
    jikkenModuleAll.ShowResult("Fer2013")



