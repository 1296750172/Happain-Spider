
import csv


class MyCsv():
    def __init__(self):
        pass


    @staticmethod
    def read(path,encoding='utf-8'):
        with open(path,'r',encoding=encoding) as f:
            data=list(csv.reader(f))
        return data

    @staticmethod
    def writerow(file,data):
        write=csv.writer(file)
        write.writerow(data)
        pass

    @staticmethod
    def writerows(file,data):
        write=csv.writer(file)
        write.writerows(data)
        pass