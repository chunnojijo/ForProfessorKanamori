import os
os.environ["USERNAME"] = "chunn"
import argparse
import cv2
import glob
import os
import time
from enum import Enum
import numpy as np
from PIL import Image
from matplotlib import pyplot
from paz.pipelines import MiniXceptionFER
import pandas as pd
import sys

class Emotion(Enum):
    angry = "angry" 
    disgust = "disgust"
    fear = "fear"
    happy = "happy"
    sad = "sad"
    surprise = "surprise"
    neutral = "neutral"

def EnableMosaic(image,eye_list,mosaicRatio,mosaicPosition):
        imageWithMosaic=image.copy()
        if mosaicPosition=="In":
            for eyeNumber in range(0,len(eye_list)):
                (x,y,w,h)=eye_list[eyeNumber]
                trim=image[y:y+h,x:x+w]
                trim=Mosaic(trim,mosaicRatio)
                imageWithMosaic[y:y+h,x:x+w]=trim
        elif mosaicPosition=="Under":
            (x,y,w,h)=eye_list[0]
            trim=image[y+h:,:]
            trim=Mosaic(trim,mosaicRatio)
            imageWithMosaic[y+h:,:]=trim
        elif mosaicPosition=="Upper":
            (x,y,w,h)=eye_list[0]
            trim=image[:y+h,:]
            trim=Mosaic(trim,mosaicRatio)
            imageWithMosaic[:y+h,:]=trim
        elif mosaicPosition=="All":
            imageWithMosaic=Mosaic(imageWithMosaic,mosaicRatio)
        np.where(np.isnan(imageWithMosaic) | np.isinf(imageWithMosaic),0,imageWithMosaic)
        return imageWithMosaic



def EnableTrim(image,eye_list,mosaicPosition):
        trim=image.copy()
        if mosaicPosition=="Under":
            (x,y,w,h)=eye_list[0]
            trim=image[y+h:,:]
        elif mosaicPosition=="Upper":
            (x,y,w,h)=eye_list[0]
            trim=image[:y+h,:]
        np.where(np.isnan(trim) | np.isinf(trim),0,trim)
        return trim

def Mosaic(trim,mosaicRatio):
    trimsizeH=trim.shape[0]
    trimsizeW=trim.shape[1]
    shrinkH=trimsizeH//mosaicRatio if trimsizeH//mosaicRatio!=0 else 1
    shrinkW=trimsizeW//mosaicRatio if trimsizeW//mosaicRatio!=0 else 1
    trim=cv2.resize(trim,(shrinkW,shrinkH))
    trim=cv2.resize(trim,(trimsizeW,trimsizeH),interpolation=cv2.INTER_NEAREST)
    return trim

def ConvertEmotionToEnum(emotionString):
    if(emotionString=='DISGUST'):
        return Emotion.disgust
    elif(emotionString=='HAPPINESS'):
        return Emotion.happy
    elif(emotionString=='ANGER'):
        return Emotion.angry
    elif (emotionString=='NEUTRAL'):
        return Emotion.neutral
    elif(emotionString=='SURPRISE'):
        return Emotion.surprise
    elif(emotionString=='SADNESS'):
        return Emotion.sad
    elif(emotionString=='FEAR'):
        return Emotion.fear
    if(emotionString=='disgust'):
        return Emotion.disgust
    elif(emotionString=='happy'):
        return Emotion.happy
    elif(emotionString=='angry'):
        return Emotion.angry
    elif (emotionString=='neutral'):
        return Emotion.neutral
    elif(emotionString=='surprise'):
        return Emotion.surprise
    elif(emotionString=='sad'):
        return Emotion.sad
    elif(emotionString=='fear'):
        return Emotion.fear
    elif(emotionString=='0'):
        return Emotion.angry
    elif(emotionString=='1'):
        return Emotion.disgust
    elif(emotionString=='2'):
        return Emotion.fear
    elif(emotionString=='3'):
        return Emotion.happy
    elif(emotionString=='4'):
        return Emotion.sad
    elif(emotionString=='5'):
        return Emotion.surprise
    elif(emotionString=='6'):
        return Emotion.neutral
    else:
        return Emotion.happy
class ImageClassifer:
    def __init__(self,mosaicMode,maxMosaicRatio):
        self.classify=MiniXceptionFER()
        self.MAX_MOSAIC_RATIO=maxMosaicRatio
        self.MosaicMode=mosaicMode
        self.emotionCorrectNumberTableNormal={Emotion.angry:0,Emotion.disgust:0,Emotion.fear:0,Emotion.happy:0,Emotion.sad:0,Emotion.surprise:0,Emotion.neutral:0}
        self.emotionCorrectNumberTableWithTrim={Emotion.angry:0,Emotion.disgust:0,Emotion.fear:0,Emotion.happy:0,Emotion.sad:0,Emotion.surprise:0,Emotion.neutral:0}
        self.emotionDetectNumberTableNormal={Emotion.angry:0,Emotion.disgust:0,Emotion.fear:0,Emotion.happy:0,Emotion.sad:0,Emotion.surprise:0,Emotion.neutral:0}
        self.emotionDetectNumberTableWithTrim={Emotion.angry:0,Emotion.disgust:0,Emotion.fear:0,Emotion.happy:0,Emotion.sad:0,Emotion.surprise:0,Emotion.neutral:0}
        
        
        self.totalDetectFaceTableWithMosaic={(Emotion.angry,2):0}
        self.totalCorrectFaceTableWithMosaic={(Emotion.angry,2):0}

        #pipeline = DetectMiniXceptionFER([args.offset, args.offset])
        self.totalNumberNotTrim=0
        self.totalNumberTrim=0
        self.correctNumberTrim=0
        self.correctNumberNotTrim=0
        self.totalNumberOfFiles=0
        for emotionEnum in Emotion:
            for i in range(2,self.MAX_MOSAIC_RATIO):
                self.totalDetectFaceTableWithMosaic[(emotionEnum,i)]=0
                self.totalCorrectFaceTableWithMosaic[(emotionEnum,i)]=0
    
    def CalculateAnalitics(self,correctEmotion,detectEmotionWithMosaic,ratio):
        self.totalDetectFaceTableWithMosaic[(correctEmotion,ratio)]+=1
        if detectEmotionWithMosaic==correctEmotion:
            self.totalCorrectFaceTableWithMosaic[(correctEmotion,ratio)]+=1


    def AddImage(self,image,correctEmotion):
        print("totalNumberOfFiles"+str(self.totalNumberOfFiles))
        print("totalNumberNotTrim"+str(self.totalNumberNotTrim))
        print(self.MosaicMode)
        self.totalNumberOfFiles+=1
        cascade=cv2.CascadeClassifier('C:/Users/chunn/Downloads/openCV3/opencv/sources/data/haarcascades/haarcascade_eye.xml')
        eye_list=cascade.detectMultiScale(image, minSize=(10, 10))
        
        #if len(result['boxes2D'])>0:
        self.totalNumberNotTrim+=1
        self.emotionDetectNumberTableNormal[correctEmotion]+=1
        detectEmotionNotTrim=ConvertEmotionToEnum(self.classify(image)['class_name'])
        print("Correct"+correctEmotion.value)
        print(detectEmotionNotTrim)
        if detectEmotionNotTrim==correctEmotion:
            self.emotionCorrectNumberTableNormal[detectEmotionNotTrim]+=1
        
        if self.MosaicMode=="All":
            for i in range(2,self.MAX_MOSAIC_RATIO):
                imageWithMosaic=Mosaic(image,i)
                detectEmotionWithMosaic=ConvertEmotionToEnum(self.classify(imageWithMosaic)['class_name'])
                self.CalculateAnalitics(correctEmotion,detectEmotionWithMosaic,i)
            return

        trim=np.zeros
        if len(eye_list)>0:
            trimedImage=EnableTrim(image,eye_list,self.MosaicMode)
            cv2.imshow("Test",trim)
            cv2.waitKey()
            cv2.destroyAllWindows()
            self.emotionDetectNumberTableWithTrim[correctEmotion]+=1
            detectEmotionWithTrim=ConvertEmotionToEnum(self.classify(trimedImage)['class_name'])
            if detectEmotionWithTrim==correctEmotion:
                self.emotionCorrectNumberTableWithTrim[correctEmotion]+=1
            for i in range(2,self.MAX_MOSAIC_RATIO):
                imageWithMosaic=EnableMosaic(image,eye_list,i,self.MosaicMode)
                cv2.imshow("Test",imageWithMosaic)
                cv2.waitKey()
                cv2.destroyAllWindows()
                #self.totalDetectFaceTableWithMosaic[(correctEmotion,i)]+=1
                detectEmotionWithMosaic=ConvertEmotionToEnum(self.classify(imageWithMosaic)['class_name'])
                self.CalculateAnalitics(correctEmotion,detectEmotionWithMosaic,i)
                #if detectEmotionWithMosaic==correctEmotion:
                #    self.totalCorrectFaceTableWithMosaic[(correctEmotion,i)]+=1
                
        
    
    
    def ShowResult(self,DatasetName):
        if self.MosaicMode!="In" and self.MosaicMode!="All":
            correctRateNormal=[]
            correctRateWithTrim=[]
            emotions=[]
            for emotionEnum in Emotion:
                emotions.append(emotionEnum.value)
                correctRateNormalTmp=0
                correctRateWithTrimTmp=0
                if self.emotionDetectNumberTableNormal[emotionEnum]==0:
                    correctRateNormalTmp=-0.1
                else:
                    correctRateNormalTmp=self.emotionCorrectNumberTableNormal[emotionEnum]/self.emotionDetectNumberTableNormal[emotionEnum]
                if self.emotionDetectNumberTableWithTrim[emotionEnum]==0:
                    correctRateWithTrimTmp=-0.1
                else:
                    correctRateWithTrimTmp=self.emotionCorrectNumberTableWithTrim[emotionEnum]/self.emotionDetectNumberTableWithTrim[emotionEnum]
                correctRateNormal.append(correctRateNormalTmp)
                correctRateWithTrim.append(correctRateWithTrimTmp)
                # correctRateNormal=np.append(correctRateNormal,self.emotionCorrectNumberTableNormal[emotionEnum]/self.emotionDetectNumberTableNormal[emotionEnum])
                # correctRateWithTrim=np.append(correctRateWithTrim,self.emotionCorrectNumberTableWithTrim[emotionEnum]/self.emotionDetectNumberTableWithTrim[emotionEnum])
            df=pd.DataFrame({'Emotion':emotions,'CorrectRate(NoMask)':correctRateNormal,'CorrectRate(WithMask)':correctRateWithTrim})[['Emotion','CorrectRate(NoMask)','CorrectRate(WithMask)']]

            table=pyplot.table(cellText=df.values,
                    colLabels=df.columns,
                    colWidths=[0.1,0.1,0.1] ,
                    loc='center')
            table.set_fontsize(50)
            pyplot.axis('off')
            table.scale(3, 3)
            pyplot.savefig("C:/Users/chunn/Pictures/特別実験/Table/"+DatasetName+self.MosaicMode+"TrimCollectTable.jpg")
            #pyplot.show()
            pyplot.close()
            
        pyplot.axis('on')
        y=np.zeros(1)
        for emotionEnum in Emotion:
            print(emotionEnum)
            if self.emotionDetectNumberTableNormal[emotionEnum]!=0:
                print("correctNumberNormal"+str(self.emotionCorrectNumberTableNormal[emotionEnum]))
                print("emotionDetectNumberTableNormal"+str(self.emotionDetectNumberTableNormal[emotionEnum]))
                print("correctRateNumberNotTrim"+str(self.emotionCorrectNumberTableNormal[emotionEnum]/self.emotionDetectNumberTableNormal[emotionEnum]))
            for i in range(1,self.MAX_MOSAIC_RATIO):
                if i==1:
                    #y2=np.array([totalDetectFaceTableWithMosaic[(emotionEnum,i)]])
                    if self.emotionCorrectNumberTableNormal[emotionEnum]!=0:
                        y=np.array([self.emotionCorrectNumberTableNormal[emotionEnum]/self.emotionDetectNumberTableNormal[emotionEnum]])
                    else:
                        y=np.array([-0.1])
                else:
                    #y2=np.append(y2,totalDetectFaceTableWithMosaic[(emotionEnum,i)])
                    if self.totalDetectFaceTableWithMosaic[(emotionEnum,i)]!=0:
                        y=np.append(y,self.totalCorrectFaceTableWithMosaic[(emotionEnum,i)]/self.totalDetectFaceTableWithMosaic[(emotionEnum,i)])
                    else:
                        y=np.append(y,-0.1)
                # if self.totalDetectFaceTableWithMosaic[(emotionEnum),i]!=0:
                #     print("correctNumberWithTrim"+str(totalCorrectFaceTableWithMosaic[(emotionEnum,i)]))
                #     print("totalDetectFaceTableWithMosaic"+str(totalDetectFaceTableWithMosaic[(emotionEnum,i)]))
                #     print("correctRateNumberWithMosaic"+str(totalCorrectFaceTableWithMosaic[(emotionEnum,i)]/totalDetectFaceTableWithMosaic[(emotionEnum,i)]))
            x=np.arange(1,self.MAX_MOSAIC_RATIO)
            fig,ax1=pyplot.subplots()
            ax1.plot(x,y,color="blue",label="CorrectRate")
            ax2=ax1.twinx()
            pyplot.title(emotionEnum.value)
            #ax2.plot(x,y2,color="green",label="detectFaceNumber")
            ax1.set_ylabel(r'$CorrectRate$')
            ax1.grid(True)
            #ax2.set_ylabel(r'$detectFaceNumber$')
            #h1, l1 = ax1.get_legend_handles_labels()
            #h2, l2 = ax2.get_legend_handles_labels()
            #ax1.legend(h1+h2, l1+l2, loc='upper right')
            if not os.path.exists("C:/Users/chunn/Pictures/特別実験/"+emotionEnum.value):
                os.makedirs("C:/Users/chunn/Pictures/特別実験/"+emotionEnum.value)
            fig.savefig("C:/Users/chunn/Pictures/特別実験/"+emotionEnum.value+"/"+DatasetName+emotionEnum.value+self.MosaicMode+"EyeIsMosaic.jpg")
            #pyplot.show()
            pyplot.close()


