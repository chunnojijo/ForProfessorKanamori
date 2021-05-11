
import os
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
from paz.models.classification import MiniXception
import JikkenModule
import sys
from tensorflow.keras.utils import plot_model

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Real-time face classifier')
    # parser.add_argument('mode')
    
    # args = parser.parse_args()
    # MosaicMode=args.mode
    # if(MosaicMode!="Upper" and MosaicMode!="Under" and MosaicMode!="In"):
    #     exit()
    files=glob.glob('C:/Users/chunn/Downloads/IMFDB_final/IMFDB_final/*')
    test_data = open("C:/Users/chunn/Downloads/MTFL/training.txt", "r")

    


    # 行ごとにすべて読み込んでリストデータにする
    lines = test_data.readlines()
    test_data.close()

    totalNumberOfFiles=0
    jikkenModuleUpper=JikkenModule.ImageClassifer(mosaicMode="Upper",maxMosaicRatio=30)
    jikkenModuleUnder=JikkenModule.ImageClassifer(mosaicMode="Under",maxMosaicRatio=30)
    jikkenModuleIn=JikkenModule.ImageClassifer(mosaicMode="In",maxMosaicRatio=30)
    jikkenModuleAll=JikkenModule.ImageClassifer(mosaicMode="All(AllImageUse)",maxMosaicRatio=30)
   
    #model=MiniXception((48, 48, 1), 7, weights='FER')
    
    #plot_model(model,to_file="C:/Users/chunn/Pictures/特別実験/model.jpg")
    for fileName1 in files:
        for fileName2 in glob.glob(fileName1+'/*'):
            fileName2.replace('\\','/')
            test=glob.glob(fileName2+'/*.txt')
            if len(test)==0:
                continue
            test_data = open(glob.glob(fileName2+'/*.txt')[0], 'r', encoding='UTF-8')
            lines = test_data.readlines()
            test_data.close()
            for line in lines:
                # totalNumberOfFiles+=1
                # if totalNumberOfFiles>100:
                #     jikkenModuleUnder.ShowResult("Indian")
                #     jikkenModuleUpper.ShowResult("Indian")
                #     jikkenModuleIn.ShowResult("Indian")
                #     sys.exit()
                words=line.split()
                if len(words)>12:
                    imageName=words[2]
                    emotion=words[11]
                    correctEmotion=JikkenModule.ConvertEmotionToEnum(emotion)
                    imagePath=fileName2+'/images/'+imageName
                    try:
                        im=Image.open(imagePath)
                    except  IOError:
                        continue
                    
                    if os.path.exists(fileName2+'/images/'+imageName):
                        
                        image=np.zeros
                        image = cv2.imread(imagePath,1)
                        try:
                            jikkenModuleAll.AddImage(image,correctEmotion)
                        except KeyboardInterrupt:
                            sys.exit()
                        
                        try:
                            jikkenModuleUnder.AddImage(image,correctEmotion)
                        except KeyboardInterrupt:
                            sys.exit()
                        except:
                            pass
                        try:
                            jikkenModuleIn.AddImage(image,correctEmotion)
                        except KeyboardInterrupt:
                            sys.exit()
                        except:
                            pass
                        try:
                            jikkenModuleUpper.AddImage(image,correctEmotion)
                        except KeyboardInterrupt:
                            sys.exit()
                        except:
                            pass
                        # internalModel=Model(inputs=classify.model.input,outputs=model.get_layer("add_4").output)

                        #plot_model(model,to_file="C:/Users/chunn/Pictures/特別実験/model.jpg")
                        # test=model.predict(img_gray)
                        # cv2.imshow(test)
                        # cv2.waitKey()
                        # cv2.destroyAllWindows()

    # jikkenModuleUnder.ShowResult("Indian")
    # jikkenModuleUpper.ShowResult("Indian")
    # jikkenModuleIn.ShowResult("Indian")
    jikkenModuleAll.ShowResult("Indian")




