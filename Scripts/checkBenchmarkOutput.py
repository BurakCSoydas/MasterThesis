from glob import glob
from os.path import isdir,dirname, realpath

import numpy


def main():
    # check if output folser exists or is empty. Exists if any is true:
    relPath2Output: str = "./output/"
    cwd: str =  dirname(realpath(__file__))
    
    if not isdir(relPath2Output):
        print(f"{relPath2Output} doesn't exist or contains no files.\nCalled from {cwd}")
        return
    
    # get all files inside output folder
    allFiles: list = glob(relPath2Output + '*.csv')
    
    # define patterns to categorize files
    EM: list = [
             'Cpp',
             'Py',
            ]

    DM: list = [
             'Cpp',
             'PyClass',
             'PyDataclass',
             'PyDict',
             'PyList',
            ]

    mode = [
            'H',
            'HL',
            'V',
            'VL',
            ]   

    # define container to collect info on DriverModelVar base
    class BenchmarkFiles:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': 0,'HL': 0,'V': 0,'VL': 0},
                              'Py': {'H': 0,'HL': 0,'V': 0, 'VL': 0}}
            self.Sim : dict = {'Cpp': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0},
                              'Py': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0}}

    class TimeFiles:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': 0,'HL': 0,'V': 0,'VL': 0},
                              'Py': {'H': 0,'HL': 0,'V': 0, 'VL': 0}}
            self.Sim : dict = {'Cpp': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0},
                              'Py': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0}}
    # create list to store container
    results : list = []

    for _, variant in enumerate(DM):
        results.append(BenchmarkFiles(variant))
    # create list to store container
    timeResults : list = []

    for _, variant in enumerate(DM):
        timeResults.append(TimeFiles(variant))
    
    # for _, obj in enumerate(results):
    #     print(obj.modelVariant,'\n', obj.DM,'\n',obj.EM)

    # DM: DMNameBenchConf-SimVar and timeDMNameBenchConfig-SimVar
    # Sim: EMSimVarBenchmode-DMName and timeEMSimVarBenchConfig-DMMode
    for result in results:
        print("-----",result.modelVariant,"-----")
        for SimVar in result.DM.keys():  
            print("DM",SimVar)
            for BenchConf in result.DM[SimVar].keys():
                # print(result.modelVariant,SimVar,BenchConf)
                for file in allFiles: 
                    if file.startswith(relPath2Output + result.modelVariant + BenchConf + "-" + SimVar):
                        result.DM[SimVar][BenchConf] += 1
                # print(result.DM[SimVar][BenchConf])

            print(result.DM[SimVar])
            print()

        for SimVar in result.Sim.keys():  
            print("Sim",SimVar)
            for BenchConf in result.Sim[SimVar].keys():
                # print(result.modelVariant,SimVar,BenchConf)
                for file in allFiles: 
                    if file.startswith(relPath2Output + 'EM' + SimVar + BenchConf + "-" + BenchConf):
                        
                        print(file)
                        result.Sim[SimVar][BenchConf] += 1
                # print(result.DM[SimVar][BenchConf])

            print(result.Sim[SimVar])
            print()

    # for timeResult in timeResults:
    #     print("-----",timeResult.modelVariant,"-----")
    #     for SimVar in timeResult.DM.keys():  
    #         print("time DM",SimVar)
    #         for BenchConf in timeResult.DM[SimVar].keys():
    #             # print(result.modelVariant,SimVar,BenchConf)
    #             for file in allFiles: 
    #                 if file.startswith(relPath2Output + 'time' + timeResult.modelVariant + BenchConf + "-" + SimVar):
    #                     print(file)
    #                     timeResult.DM[SimVar][BenchConf] += 1
    #             # print(result.DM[SimVar][BenchConf])
    #
    #         print(timeResult.DM[SimVar])
    #         print()
    #     for SimVar in result.Sim.keys():  
    #         print("Sim",SimVar)
    #         for BenchConf in result.Sim[SimVar].keys():
    #             # print(result.modelVariant,SimVar,BenchConf)
    #             for file in allFiles: 
    #                 if file.startswith(relPath2Output + result.modelVariant + BenchConf + "-" + SimVar):
    #                     result.Sim[SimVar][BenchConf] += 1
    #             # print(result.DM[SimVar][BenchConf])
    #
    #         print(result.Sim[SimVar])
    #         print()

    
    
            # for file in allFiles: 
            #     print(file)

        print()


    print(len(allFiles), type(allFiles[1])) 
if __name__ == "__main__":
    main()
