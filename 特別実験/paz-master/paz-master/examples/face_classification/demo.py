import argparse
from paz.backend.camera import VideoPlayer
from paz.backend.camera import Camera
from paz.pipelines import DetectMiniXceptionFER
import cv2
import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Real-time face classifier')
    parser.add_argument('-c', '--camera_id', type=int, default=0,
                        help='Camera device ID')
    parser.add_argument('-o', '--offset', type=float, default=0.1,
                        help='Scaled offset to be added to bounding boxes')
    args = parser.parse_args()

    files=glob.glob('C:/Users/chunn/Downloads/MTFL/lfw_5590/*')
    test_data = open("C:/Users/chunn/Downloads/MTFL/training.txt", "r")

    # 行ごとにすべて読み込んでリストデータにする
    lines = test_data.readlines()
    test_data.close()
    
    totalWearingGlassIncludeNotDetect=0
    totalWearingGlassIncludeOnlyDetect=0
    correctWearingGlass=0
    totalNotWearingGlassIncludeNotDetect=0
    totalNotWearingGlassIncludeOnlyDetect=0
    correctNotWearingGlass=0
    
    pipeline = DetectMiniXceptionFER([args.offset, args.offset])

    for number in range(0,len(files)):
        info=lines[number].split()
        
        isSmile=info[12]=='1'
        isWearingGlass=info[13]=='1'
        
        if isWearingGlass :
            totalWearingGlassIncludeNotDetect+=1
        else:
            totalNotWearingGlassIncludeNotDetect+=1
        image = cv2.imread(files[number],1)
        result=pipeline(image)
        if len(result['boxes2D'])==0:
            continue
        
        if isWearingGlass :
            totalWearingGlassIncludeOnlyDetect+=1
        else:
            totalNotWearingGlassIncludeOnlyDetect+=1
        isDetectSmile=result['boxes2D'][0].class_name=='happy'
        #isDetectSmile=emotion.happiness==max([emotion.anger,emotion.contempt,emotion.disgust,emotion.fear,emotion.happiness,emotion.neutral,emotion.sadness,emotion.surprise])
        if isDetectSmile==isSmile :
            if isWearingGlass :
                #print("CorrectWearingGlass")
                correctWearingGlass+=1
            else:
                #print("CorrectNotWearingGlass")
                correctNotWearingGlass+=1
        print(str(number)+'/'+str(len(files)))
        print(result['boxes2D'][0].class_name)
        

    print("correctWearingGlass")
    print(correctWearingGlass/totalWearingGlassIncludeNotDetect)
    print("corretNotWearingGlass")
    print(correctNotWearingGlass/totalNotWearingGlassIncludeNotDetect)
    print("totalWearingGlassIncludeNotDetect"+str(totalWearingGlassIncludeNotDetect))
    print("totalNotWearingGlassIncludeNotDetect"+str(totalNotWearingGlassIncludeNotDetect))
    print("correctWearingGlass"+str(correctWearingGlass))
    print("totalWearingGlassIncludeOnlyDetect"+str(totalWearingGlassIncludeOnlyDetect))
    print("correctWearingGlass")
    print(correctWearingGlass/totalWearingGlassIncludeOnlyDetect)
    print("correctNotWearingGlass"+str(correctNotWearingGlass))
    print("totalNotWearingGlassIncludeOnlyDetect"+str(totalNotWearingGlassIncludeOnlyDetect))
    print("corretNotWearingGlass")
    print(correctNotWearingGlass/totalNotWearingGlassIncludeOnlyDetect)
        
    
