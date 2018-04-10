import glob
from shutil import copyfile
import platform

class CKPlusOrganizer:

    def __init__(self):
        OS = platform.system()
        if OS=="Windows":
            raise Exception("This file was originally written for Linux/MacOS. Please replace all '/' with '\\' in dataset_organiser.py")


    def make_structure(self, source_emotion='source_emotion', source_images='source_images', dataset='sorted_set'):
        try:
            emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
            secicipants = glob.glob(str(source_emotion)+"/*")
            for x in secicipants:
                sec = "%s" %x[-4:]
                for sessions in glob.glob("%s/*" %x):
                    for files in glob.glob("%s/*" %sessions):
                        curr_session = files[20:-30]
                        file = open(files, 'r')
                        emotion = int(float(file.readline()))
                        source_emotion = glob.glob(str(source_images)+"/%s/%s/*" %(sec, curr_session))[-1]
                        source_neutral = glob.glob(str(source_images)+"/%s/%s/*" %(sec, curr_session))[0]
                        dest_neut = str(dataset)+"/neutral/%s" %source_neutral[25:]
                        dest_emot = str(dataset)+"/%s/%s" %(emotions[emotion], source_emotion[25:])
                        copyfile(source_neutral, dest_neut)
                        copyfile(source_emotion, dest_emot)
            print("Structured Dataset has been created in directory-> "+str(dataset))
        except Exception as e:
            print(e)
