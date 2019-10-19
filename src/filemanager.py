import os, stat, hashlib
import datetime, time
import csv

class FileManager:

    def __init__(self):
        self.__path_list = []
        self.dup_filelist = {}
    def scan(self, path):
        print('Start to scan files in path: ' + path)
        self.__path_list.append(path)
        l = sum(len(files) for root, dirs, files in os.walk(path))
        i = 0
        printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                fname = os.path.join(root, name)
                fi = FileInfo(fname)
                if fi.checksum in self.dup_filelist:
                    flist = self.dup_filelist[fi.checksum]
                    flist.add(fi.path)
                else:
                    self.dup_filelist[fi.checksum] = set({fi.path,})
                i += 1
                printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            
    
    def dump_duplicated(self, csvpath):
        print('Start to dump the duplicated file list to: ' + csvpath)
        l = len(self.dup_filelist)
        i = 0
        printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        with open(csvpath, 'w', newline='',encoding='utf-8-sig') as dup:
            w = csv.writer(dup)
            for key, val in self.dup_filelist.items():
                count = len(val)
                if count > 1:
                    for f in val:
                        w.writerow(list((key, count, f)))
                printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
                i += 1
    
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

class FileInfo:
    __checksum = ''
    __size = 0
    def __init__(self, filename):
        self.path = filename
        self.name = filename.split('\\')[-1]
        self.__filestat = os.stat(filename)
    
    @property
    def checksum(self):
        if(self.__checksum == ''):
            self.__checksum = self.__get_checksum()
        return self.__checksum
    @property
    def size(self):
        if self.__filestat is None:
            self.__size = self.__filestat [stat.ST_SIZE]
        return 0
    
    @property 
    def created_date(self):
        return time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(self.__filestat[stat.ST_CTIME]))

    @property
    def modified_date(self):
        return time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(self.__filestat[stat.ST_MTIME]))
    
    def __get_checksum(self):
        hash_md5 = hashlib.md5(open(self.path,'rb').read())
        return hash_md5.hexdigest()
    

 
    