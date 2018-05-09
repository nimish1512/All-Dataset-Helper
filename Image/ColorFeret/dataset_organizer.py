import os
import argparse
import bz2
import multiprocessing
import shutil
import sys


class TaskParser:

    def __init__(self,task,gt_path,tar_path):
        self.task=task
        self.classes = list()
        self.pwd = os.getcwd()
        flag=0
        self.data = {}
        self.tar_path = tar_path
        for d,r,f in os.walk(gt_path):
            if flag:
                temp1 = d.split('/')
                self.data.update({temp1[-1]:f})
            else:
                self.path = d
                flag=1
        self.dataset_path = os.getcwd()+'/dataset'
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)

    def read_mono_data(self):
        if self.task=='gender':
            if not os.path.exists(self.dataset_path+'/gender/male'):
                os.makedirs(self.dataset_path+'/gender')
                os.makedirs(self.dataset_path+'/gender/male')
                os.makedirs(self.dataset_path+'/gender/female')
            male_samples = list()
            female_samples = list()
            for k,v in self.data.items():
                with open(self.path+'/'+k+'/'+k+'.txt') as f:
                    file_content = f.readline()
                    file_content = f.readline()
                    file_content = file_content.replace('\n','').split('=')
                    if file_content[1].lower()=='male':
                        male_samples.append(k)
                    else:
                        female_samples.append(k)
            print("Found {0} male samples\nFound {1} femle samples".format(len(male_samples),len(female_samples)))
            del_opt = input("Before copying images to target_class folders, do you wish to delete original images?\nType 'y' to delete and 'n' to keep them ==> ")
            print("\n\n")
            if del_opt.lower()=='n':
                for sample in female_samples:
                    for _,_,files in os.walk(self.tar_path+'/'+sample):
                        for f in files:
                            if f[-4:]==".ppm":
                                sys.stdout.flush()
                                shutil.copyfile(self.tar_path+'/'+sample+'/'+f,self.pwd+'/dataset/gender/female/'+f)
                                sys.stdout.write("Copying file %s to /dataset/gender/female          \r"%(f))

                for sample in male_samples:
                    for _,_,files in os.walk(self.tar_path+'/'+sample):
                        for f in files:
                            if f[-4:]==".ppm":
                                sys.stdout.flush()
                                shutil.copyfile(self.tar_path+'/'+sample+'/'+f,self.pwd+'/dataset/gender/male/'+f)
                                sys.stdout.write("Copying file %s to /dataset/gender/male            \r"%(f))
            else:
                for sample in female_samples:
                    for _,_,files in os.walk(self.tar_path+'/'+sample):
                        for f in files:
                            if f[-4:]==".ppm":
                                sys.stdout.flush()
                                os.rename(self.tar_path+'/'+sample+'/'+f,self.pwd+'/dataset/gender/female/'+f)
                                sys.stdout.write("Moving file %s to /dataset/gender/female           \r"%(f))

                for sample in male_samples:
                    for _,_,files in os.walk(self.tar_path+'/'+sample):
                        for f in files:
                            if f[-4:]==".ppm":
                                sys.stdout.flush()
                                os.rename(self.tar_path+'/'+sample+'/'+f,self.pwd+'/dataset/gender/male/'+f)
                                sys.stdout.write("Moving file %s to /dataset/gender/male             \r"%(f))
            sys.stdout.flush()
        elif self.task=="sunglass":
            if not os.path.exists(self.dataset_path+'/sunglass/sunglass_on'):
                os.makedirs(self.dataset_path+'/sunglass')
                os.makedirs(self.dataset_path+'/sunglass/sunglass_on')
                os.makedirs(self.dataset_path+'/sunglass/sunglass_off')
            s_on_samples = list()
            s_off_samples = list()
            for k,v in self.data.items():
                for file in v:
                    if file!=k+".txt":
                        fp = open(self.path+'/'+k+'/'+file)
                        for i,line in enumerate(fp):
                            if i==13:
                                temp = line.split('=')
                                temp1 = ""
                                if temp[-1]=='Yes\n':
                                    s_on_samples.append(file[:-4]+'.ppm')
                                elif temp[-1]=="No\n":
                                    s_off_samples.append(file[:-4]+'.ppm')
                                del temp1
                        fp.close()
            print("Found {0} Sunglass_on samples\nFound {1} Sunglass_off samples".format(len(s_on_samples),len(s_off_samples)))
            del_opt = input("Before copying images to target_class folders, do you wish to delete original images?\nType 'y' to delete and 'n' to keep them ==> ")
            print("\n\n")
            if del_opt.lower()=='n':
                for sample in s_off_samples:
                    folder_name = sample.split('_')
                    folder_name = folder_name[0]
                    sys.stdout.flush()
                    shutil.copyfile(self.tar_path+'/'+folder_name+'/'+sample,self.pwd+'/dataset/sunglass/sunglass_off/'+sample)
                    sys.stdout.write("Copying file %s to /dataset/sunglass/sunglass_off          \r"%(sample))                    

                for sample in s_on_samples:
                    folder_name = sample.split('_')
                    folder_name = folder_name[0]
                    sys.stdout.flush()
                    shutil.copyfile(self.tar_path+'/'+folder_name+'/'+sample,self.pwd+'/dataset/sunglass/sunglass_on/'+sample)
                    sys.stdout.write("Copying file %s to /dataset/sunglass/sunglass_on          \r"%(sample))
            elif del_opt.lower()=='y':
                for sample in s_off_samples:
                    folder_name = sample.split('_')
                    folder_name = folder_name[0]
                    sys.stdout.flush()
                    os.rename(self.tar_path+'/'+folder_name+'/'+sample,self.pwd+'/dataset/sunglass/sunglass_off/'+sample)
                    sys.stdout.write("Copying file %s to /dataset/sunglass/sunglass_off          \r"%(sample))                    

                for sample in s_on_samples:
                    folder_name = sample.split('_')
                    folder_name = folder_name[0]
                    sys.stdout.flush()
                    os.rename(self.tar_path+'/'+folder_name+'/'+sample,self.pwd+'/dataset/sunglass/sunglass_on/'+sample)
                    sys.stdout.write("Copying file %s to /dataset/sunglass/sunglass_on          \r"%(sample))
            sys.stdout.flush()






class DatasetOrganizer:

    def __init__(self):
        try:
            self.parser = argparse.ArgumentParser(description="Process task for dataset")
            self.supported_tasks = ['gender', 'age', 'face-features', 'sunglass']
            self.parser.add_argument('--task',help="Describes the task for which dataset should be structured")
            self.task = self.parser.parse_args()
            if self.task.task not in self.supported_tasks:
                raise ValueError("Undefined task {0}".format(self.task.task))
            self.pwd = os.getcwd()
            divs = ['dvd1','dvd2']
            file_list = {}
            flag=0
            self.task_parsers = list()
            for sec in divs:
                self.task_parsers.append(TaskParser(self.task.task,self.pwd+'/colorferet/'+sec+'/data/ground_truths/name_value',self.pwd+'/colorferet/'+sec+'/data/images'))
                temp = list()
                for dir_names, root, filenames in os.walk(self.pwd+'/colorferet/'+sec+'/data/images'):
                    if flag:
                        temp.append([dir_names+'/'+s for s in filenames])
                    else:
                        flag=1
                flag=0
                file_list.update({sec:temp})
                del temp
            for parser in self.task_parsers:
                parser.read_mono_data()
            print("Dataset created")
            '''         
            self.processes = list()
            queue = multiprocessing.Queue()
            for k in divs:
                self.processes.append(multiprocessing.Process(target=decompress, args=(file_list[k],queue)))
            for i,proc in enumerate(self.processes):
                proc.start()
                print("Started process {0} for dvd{1}.....".format(i+1,i+1))
            print("Please be patient as this might take a while depending on your system's config...")
            for proc in self.processes:
                proc.join()
            result1 = queue.get()
            result2 = queue.get()
            print("Decompressed {0} files".format(result1+result2))
            '''
        except Exception as e:
            print(e)
            pass


    


def decompress(files, queue):
    cntr = 0
    try:
        for parent_dir in files:
            for file in parent_dir:
                if file[:-4]!='.ppm':
                    zip_img = bz2.BZ2File(file)
                    data = zip_img.read()
                    decoded_img = file[:-4]
                    with open(decoded_img,'wb') as f:
                        f.write(data)
                    cntr+=1
                else:
                    print("Skipped {0}".format(file))
        print("Returning {0} files ".format(cntr))
        queue.put(cntr)
    except Exception as e:
        print(e)
        pass
    




if __name__=="__main__":
    x = DatasetOrganizer()
#   print(os.getcwd())