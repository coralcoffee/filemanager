import filemanager
import datetime
def main():

    targetDirs = [r'C:\Live\英文书籍']

    start = datetime.datetime.now()
    fm = filemanager.FileManager()
    for p in targetDirs:
        fm.scan(p)
    
    fm.dump_duplicated("dup.csv")
    end = datetime.datetime.now()
    print('Total time is: ' + str(end - start))


if __name__ == '__main__':
    main()