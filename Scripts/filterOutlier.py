from glob import glob
from os.path import isdir,dirname, realpath
from os import path, makedirs
import numpy as np


def main():
    # check if output folser exists or is empty. Exists if any is true:
    relPath2Output: str = "./output/"
    cwd: str =  dirname(realpath(__file__))
    
    if not isdir(relPath2Output):
        print(f"{relPath2Output} doesn't exist or contains no files.\nCalled from {cwd}")
        return
    
    # get all files inside output folder
    allFiles: list = glob(relPath2Output + '*.csv')
    if not path.exists('./filteredData/'):
        makedirs('./filteredData/')
    print("Removing outliers from Benchmarks using IQR.")   
    for file in allFiles:
        data = np.genfromtxt(file,delimiter=',',dtype='float64')
        sortedData = np.sort(data[1:])
        fileName = file.split('/')
        if not file.startswith('./output/time'):
            q1 = np.percentile(sortedData, 25)
            q3 = np.percentile(sortedData, 75)
            iqr = q3 - q1
            threshold = 1.5 * iqr
            outlier = np.where((sortedData < q1 - threshold) | (sortedData > q3 + threshold))
            filteredData = np.delete(sortedData,outlier)
        else:
            filteredData = data

        print(filteredData.shape)
        np.save('./filteredData/' + fileName[-1], filteredData,allow_pickle=False) 

    print("Removed outliers from Benchmarks using IQR. Stored filtered data in ./filteredData/. ")
    # print('\n',len(allFiles), type(allFiles[1])) 
if __name__ == "__main__":
    main()
