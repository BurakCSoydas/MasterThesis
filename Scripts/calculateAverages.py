# idea to use in thesis report: Use varaince and argue that python esmini had bigger variance
# print(allDMloops.mean(),allDMloops.std(), allDMloops.var()) 
from glob import glob
from os.path import isdir,dirname, realpath
from os import path, makedirs

import numpy as np
import matplotlib.pyplot as plt


def main():
    print("Started creation of tables showing averages and histograms.\n")
    # check if output folser exists or is empty. Exists if any is true:
    source: str = "./filteredData/"
    cwd: str =  dirname(realpath(__file__))
    
    if not isdir(source):
        print(f"{source} doesn't exist or contains no files.\nCalled from {cwd}")
        return
    
    print("Preparing data objects.\n")
    # get all files inside output folder
    allFiles: list = glob(source + '*.npy')

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
    class AllInOne:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': 0,'HL': 0,'V': 0,'VL': 0},
                              'Py': {'H': 0,'HL': 0,'V': 0, 'VL': 0}}
            self.Sim : dict = {'Cpp': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0},
                              'Py': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0}}
    class Cache:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': {},'HL': {},'V': {},'VL': {}},
                              'Py': {'H': {},'HL': {},'V': {}, 'VL': {}}}
            self.Sim : dict = {'Cpp': {'H': {}, 'HL': {}, 'V': {}, 'VL': {}},
                              'Py': {'H': {}, 'HL': {}, 'V': {}, 'VL': {}}}
    class Averages:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': 0,'HL': 0,'V': 0,'VL': 0},
                              'Py': {'H': 0,'HL': 0,'V': 0, 'VL': 0}}
            self.Sim : dict = {'Cpp': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0},
                              'Py': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0}}

    class TimeTimes:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': 0,'HL': 0,'V': 0,'VL': 0},
                              'Py': {'H': 0,'HL': 0,'V': 0, 'VL': 0}}
            self.Sim : dict = {'Cpp': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0},
                              'Py': {'H': 0, 'HL': 0, 'V': 0, 'VL': 0}}

    class Edges:
        def __init__(self, modelVariant: str):
            self.modelVariant : str = modelVariant
            self.DM : dict = {'Cpp': {'H': [999999, 0],'HL': [999999, 0],'V': [999999, 0],'VL': [999999, 0]},
                              'Py': {'H': [999999, 0],'HL': [999999, 0],'V': [999999, 0], 'VL': [999999, 0]}}
            self.Sim : dict = {'Cpp': {'H': [999999, 0], 'HL': [999999, 0], 'V': [999999, 0], 'VL': [999999, 0]},
                              'Py': {'H': [999999, 0], 'HL': [999999, 0], 'V': [999999, 0], 'VL': [999999, 0]}}
    # create list to store container
    results = [Averages(variant) for variant in DM]

    # create list to store container
    timeResults = [TimeTimes(variant) for variant in DM]

    # create list to store edges for better histograms
    edges = [Edges(variant) for variant in DM]

    # create list to store each file to use for histograms creation
    caches = [Cache(variant) for variant in DM]

    # create list to store each file in one array to use for histograms creation
    AllInOnes = [AllInOne(variant) for variant in DM]

    print("Creating folder 'histograms'.\n")
    # create dictionary to store histograms in
    if not path.exists('./histograms/'):
      makedirs('./histograms/')

    print("Loading filtered data.\n")
    # loop driver model var
    for ind,result in enumerate(results):
        # create subfolder to organize histograms
        if not path.exists('./histograms/' + result.modelVariant):
             makedirs('./histograms/' + result.modelVariant)

        print('--- ' + result.modelVariant +  '---')

        # loop SimVar
        for SimVar in EM:
            # loop all BenchMode, 
            for BenchMode in mode:
                resetDM = True
                allSingleDMloops = {}
                countDMFiles = 0
                resetSim = True
                allSingleSIMloops = {}
                countSIMFiles = 0
                
                # loop all files, sort them and collect values in a single array 
                for file in allFiles:
                    # DM files
                    if file.startswith(source + result.modelVariant + BenchMode + '-' + SimVar):
                        # load filtered data
                        data = np.load(file)
                        # append values of data
                        allSingleDMloops[str(countDMFiles)] = data

                        countDMFiles += 1
                        # check and update MinMaxMatches for given Simvar + BenchMode
                        edges[ind].DM[SimVar][BenchMode] = [ min([data.min(),edges[ind].DM[SimVar][BenchMode][0]]), max([data.max(),edges[ind].DM[SimVar][BenchMode][1]]) ]
                        # check if new DM + SimVar + BenchMode combo started
                        if resetDM:
                            AllInOnes[ind].DM[SimVar][BenchMode] = data
                            resetDM = False
                        else:
                            AllInOnes[ind].DM[SimVar][BenchMode] = np.append(AllInOnes[ind].DM[SimVar][BenchMode],data)

                    # SIM files
                    if file.startswith(source + 'EM' + SimVar + BenchMode + '-' + result.modelVariant):
                        # load filtered data
                        data = np.load(file)
                        # append values of data
                        allSingleSIMloops[str(countSIMFiles)] = data

                        countSIMFiles += 1
                        # check and update MinMaxMatches for given Simvar + BenchMode
                        edges[ind].Sim[SimVar][BenchMode] = [ min([data.min(),edges[ind].Sim[SimVar][BenchMode][0]]), max([data.max(),edges[ind].Sim[SimVar][BenchMode][1]]) ]
                        # check if new DM + SimVar + BenchMode combo started
                        if resetSim:
                            AllInOnes[ind].Sim[SimVar][BenchMode] = data
                            resetSim = False
                        else:
                            AllInOnes[ind].Sim[SimVar][BenchMode] = np.append(AllInOnes[ind].Sim[SimVar][BenchMode],data)


                    # DM TIME files
                    if (file.startswith(source + 'time' + result.modelVariant + BenchMode + '-' + SimVar) and not file.startswith(source + 'timeEM')):
                        # load filtered data
                        data = np.load(file)
                        # data[np.where(data == 0)] = 0.0044
                        avgTime = np.average(data,axis=0) 
                        data_str = np.array2string(avgTime, precision=2, separator=' ', max_line_width=35)
                        timeResults[ind].DM[SimVar][BenchMode] = data_str[1:-1] 
                    # Sim TIME files
                    if file.startswith(source + 'timeEM' + SimVar + BenchMode + '-' + result.modelVariant):
                        # load filtered data
                        data = np.load(file)
                        # data[np.where(data == 0)] = 0.0044
                        avgTime = np.average(data,axis=0) 
                        data_str = np.array2string(avgTime, precision=2, separator=' ', max_line_width=35)
                        timeResults[ind].Sim[SimVar][BenchMode] = data_str[1:-1]
               
                print(f"Loaded data for {result.modelVariant} {SimVar} {BenchMode}.\n")
                # cahce single sim data to create histogram of single runs later
                caches[ind].DM[SimVar][BenchMode] = allSingleDMloops
                caches[ind].Sim[SimVar][BenchMode] = allSingleSIMloops

                print(f":: stored Cache for individual histograms and histogram containing all.\n")
                
                # calculate average and store
                result.DM[SimVar][BenchMode] = AllInOnes[ind].DM[SimVar][BenchMode].mean()
                result.Sim[SimVar][BenchMode] = AllInOnes[ind].Sim[SimVar][BenchMode].mean()

                print(":: Calculated averages.\n")
                # # Debugging
                # print(f"\n==={result.modelVariant}{SimVar} {BenchMode}\n")
                # print(f"caches['{ind}'].DM['{SimVar}']['{BenchMode}']\n:: length ",len(caches[ind].DM[SimVar][BenchMode]),"\n:: type ",type(caches[ind].DM[SimVar][BenchMode]),f"\n:: caches['{ind}'].DM['{SimVar}']['{BenchMode}']['0']\n:::: shape ",caches[ind].DM[SimVar][BenchMode]['0'].shape,"\n:::: type ", type(caches[ind].DM[SimVar][BenchMode]['0']))
                # print(f"\nAllInOnes[{ind}].DM['{SimVar}']['{BenchMode}']\n:: shape ",AllInOnes[ind].DM[SimVar][BenchMode].shape)
                # print(f"\nedges[{ind}].DM['{SimVar}']['{BenchMode}']\n:: length ", len(edges[ind].DM[SimVar][BenchMode]),'\n:: Min|Max ',edges[ind].DM[SimVar][BenchMode])
                # print(f"\nresult.DM['{SimVar}']['{BenchMode}']\n:: average ", result.DM[SimVar][BenchMode])
    
    print("Creating folder './averages/'.\n")
    if not path.exists('./averages/'):
      makedirs('./averages/')

    print("Storing calculated averages as CSV files in './averages/'.\n")
    for result in results:
        with open('./averages/' + result.modelVariant, 'w') as f:
            f.writelines(f'avg. Loop {result.modelVariant};headless;headless+log;visual;visual+log\n')
            f.writelines(f'C++;{result.Sim["Cpp"]["H"]:.2f};{result.Sim["Cpp"]["HL"]:.3f};{result.Sim["Cpp"]["V"]:.2f};{result.Sim["Cpp"]["VL"]:.2f}\n')
            f.writelines(f'{result.modelVariant};{result.DM["Cpp"]["H"]:.2f};{result.DM["Cpp"]["HL"]:.2f};{result.DM["Cpp"]["V"]:.2f};{result.DM["Cpp"]["VL"]:.2f}\n')
            f.writelines(f'{result.modelVariant};{result.DM["Py"]["H"]:.2f};{result.DM["Py"]["HL"]:.2f};{result.DM["Py"]["V"]:.2f};{result.DM["Py"]["VL"]:.2f}\n')
            f.writelines(f'Python;{result.Sim["Py"]["H"]:.2f};{result.Sim["Py"]["HL"]:.2f};{result.Sim["Py"]["V"]:.2f};{result.Sim["Py"]["VL"]:.2f}\n')

    for result in timeResults:
        with open('./averages/time' + result.modelVariant, 'w') as f:
            f.writelines(f'time command {result.modelVariant};headless;headless+log;visual;visual+log\n')
            f.writelines(f'C++;{result.Sim["Cpp"]["H"]};{result.Sim["Cpp"]["HL"]};{result.Sim["Cpp"]["V"]};{result.Sim["Cpp"]["VL"]}\n')
            f.writelines(f'{result.modelVariant};{result.DM["Cpp"]["H"]};{result.DM["Cpp"]["HL"]};{result.DM["Cpp"]["V"]};{result.DM["Cpp"]["VL"]}\n')
            f.writelines(f'{result.modelVariant};{result.DM["Py"]["H"]};{result.DM["Py"]["HL"]};{result.DM["Py"]["V"]};{result.DM["Py"]["VL"]}\n')
            f.writelines(f'Python;{result.Sim["Py"]["H"]};{result.Sim["Py"]["HL"]};{result.Sim["Py"]["V"]};{result.Sim["Py"]["VL"]}\n')        

    # # determine the edges to be used by all histograms for given Sim + Bench varitation
    glEDGES = Edges('global')
    print("\nglobal eddges") 
    # Loop SimVar
    for firstKey in glEDGES.DM.keys():
        # Loop BenchMode
        for secondKey in glEDGES.DM[firstKey]:
            glEDGES.DM[firstKey][secondKey] = [ 
                min(edges[0].DM[firstKey][secondKey][0],edges[1].DM[firstKey][secondKey][0],edges[2].DM[firstKey][secondKey][0],edges[3].DM[firstKey][secondKey][0],edges[4].DM[firstKey][secondKey][0]),
                max(edges[0].DM[firstKey][secondKey][1],edges[1].DM[firstKey][secondKey][1],edges[2].DM[firstKey][secondKey][1],edges[3].DM[firstKey][secondKey][1],edges[4].DM[firstKey][secondKey][1])]
            print(f':: {firstKey}, {secondKey}: {glEDGES.DM[firstKey][secondKey]}\n')
            glEDGES.Sim[firstKey][secondKey] = [ 
                min(edges[0].Sim[firstKey][secondKey][0],edges[1].Sim[firstKey][secondKey][0],edges[2].Sim[firstKey][secondKey][0],edges[3].Sim[firstKey][secondKey][0],edges[4].Sim[firstKey][secondKey][0]),
                max(edges[0].Sim[firstKey][secondKey][1],edges[1].Sim[firstKey][secondKey][1],edges[2].Sim[firstKey][secondKey][1],edges[3].Sim[firstKey][secondKey][1],edges[4].Sim[firstKey][secondKey][1])]
            print(f':: {firstKey}, {secondKey}: {glEDGES.Sim[firstKey][secondKey]}\n')
    # print('\n',len(allFiles)) 
    print("Creating histograms of individual runs and total of those runs.\n")
    expectedNr = 648
    expectedNrTotal = expectedNr*100
    # create histograms
    for ind,result in enumerate(results):
        if not path.exists('./histograms/' + result.modelVariant + '/SingleRun'):
            makedirs('./histograms/' + result.modelVariant + '/SingleRun')
        # loop SimVar
        for SimVar in EM:
            # loop all BenchMode, 
            for BenchMode in mode:

                # print(AllInOnes[ind].modelVariant, SimVar, BenchMode,"{:.2g}".format(((1-AllInOnes[ind].DM[SimVar][BenchMode].size/expectedNr)*100)))

                # create histogram of global data, using local edges
                print(result.modelVariant, SimVar, BenchMode)
                print(":: Creating histogram of all runs.\n")
                # DM global, local edges
                plt.hist(AllInOnes[ind].DM[SimVar][BenchMode], 100, histtype='bar')                    
                figuretitle = 'DM: ' + result.modelVariant + ' Sim: ' + SimVar + ' BenchToggle: ' + BenchMode
                plt.title(figuretitle)
                plt.xlabel(r'Benched time [$\mu$sec]')
                plt.ylabel("count")
                meanVal = AllInOnes[ind].DM[SimVar][BenchMode].mean()
                plt.axvline(x=meanVal,ls=':', color='purple')
                limitY = plt.ylim()
                plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                plt.xlim(edges[ind].DM[SimVar][BenchMode])
                limitX = plt.xlim()
                plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-AllInOnes[ind].DM[SimVar][BenchMode].size/expectedNrTotal)*100)))

                # plt.xlim([min(classwideEdges.DM['Cpp'][BenchMode][0],classwideEdges.DM['Py'][BenchMode][0]),max(classwideEdges.DM['Cpp'][BenchMode][1],classwideEdges.DM['Py'][BenchMode][1])])
                plt.savefig('./histograms/' + result.modelVariant + f'/{SimVar}-{BenchMode}.pdf')
                plt.clf()

                # Sim global, local edges
                plt.hist(AllInOnes[ind].Sim[SimVar][BenchMode], 100, histtype='bar')                    
                figuretitle = 'Sim: ' + SimVar + ' DM: ' + result.modelVariant + ' BenchToggle: ' + BenchMode
                plt.title(figuretitle)
                plt.xlabel(r'Benched time [$\mu$sec]')
                plt.ylabel("count")
                meanVal = AllInOnes[ind].Sim[SimVar][BenchMode].mean()
                plt.axvline(x=meanVal,ls=':', color='purple')
                limitY = plt.ylim()
                plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                plt.xlim(edges[ind].Sim[SimVar][BenchMode])
                limitX = plt.xlim()
                plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-AllInOnes[ind].Sim[SimVar][BenchMode].size/expectedNrTotal)*100)))
                # plt.xlim([min(classwideEdges.DM['Cpp'][BenchMode][0],classwideEdges.DM['Py'][BenchMode][0]),max(classwideEdges.DM['Cpp'][BenchMode][1],classwideEdges.DM['Py'][BenchMode][1])])
                plt.savefig('./histograms/' + result.modelVariant + f'/EM{SimVar}-{BenchMode}.pdf')
                plt.clf()

                # create histogram of global data, using global edges
                # DM global, global edges
                plt.hist(AllInOnes[ind].DM[SimVar][BenchMode], 100, histtype='bar')                    
                figuretitle = 'DM: ' + result.modelVariant + ' Sim: ' + SimVar + ' BenchToggle: ' + BenchMode
                plt.title(figuretitle)
                plt.xlabel(r'Benched time [$\mu$sec]')
                plt.ylabel("count")
                meanVal = AllInOnes[ind].DM[SimVar][BenchMode].mean()
                plt.axvline(x=meanVal,ls=':', color='purple')
                limitY = plt.ylim()
                plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                # plt.xlim(classwideEdges.DM[SimVar][BenchMode])
                plt.xlim([min(glEDGES.DM['Cpp'][BenchMode][0],glEDGES.DM['Py'][BenchMode][0]),max(glEDGES.DM['Cpp'][BenchMode][1],glEDGES.DM['Py'][BenchMode][1])])
                limitX = plt.xlim()
                plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-AllInOnes[ind].DM[SimVar][BenchMode].size/expectedNrTotal)*100)))
                plt.savefig('./histograms/' + result.modelVariant + f'/CE{SimVar}-{BenchMode}.pdf')
                plt.clf()

                # Sim global, global edges
                plt.hist(AllInOnes[ind].Sim[SimVar][BenchMode], 100, histtype='bar')                    
                figuretitle = ' Sim: ' + SimVar + ' DM: ' + result.modelVariant + ' BenchToggle: ' + BenchMode
                plt.title(figuretitle)
                plt.xlabel(r'Benched time [$\mu$sec]')
                plt.ylabel("count")
                meanVal = AllInOnes[ind].Sim[SimVar][BenchMode].mean()
                plt.axvline(x=meanVal,ls=':', color='purple')
                limitY = plt.ylim()
                plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                # plt.xlim(classwideEdges.DM[SimVar][BenchMode])
                plt.xlim([min(glEDGES.Sim['Cpp'][BenchMode][0],glEDGES.Sim['Py'][BenchMode][0]),max(glEDGES.Sim['Cpp'][BenchMode][1],glEDGES.Sim['Py'][BenchMode][1])])
                limitX = plt.xlim()
                plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-AllInOnes[ind].Sim[SimVar][BenchMode].size/expectedNrTotal)*100)))
                plt.savefig('./histograms/' + result.modelVariant + f'/CEEM{SimVar}-{BenchMode}.pdf')
                plt.clf()

                print(":: Creating histograms of single run.\n")
                for key in caches[ind].DM[SimVar][BenchMode]:
                    # single DM, global edges
                    plt.hist(caches[ind].DM[SimVar][BenchMode][key], 10, histtype='bar')                    
                    figuretitle = 'DM: ' + result.modelVariant + ' Sim: ' + SimVar + ' BenchToggle: ' + BenchMode + ' Sim #: ' + key
                    plt.title(figuretitle)
                    plt.xlabel(r'Benched time [$\mu$sec]')
                    plt.ylabel("count")
                    meanVal = caches[ind].DM[SimVar][BenchMode][key].mean()
                    plt.axvline(x=meanVal,ls=':', color='purple')
                    limitY = plt.ylim()
                    # print(limitY)
                    plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                    plt.xlim([min(glEDGES.DM['Cpp'][BenchMode][0],glEDGES.DM['Py'][BenchMode][0]),max(glEDGES.DM['Cpp'][BenchMode][1],glEDGES.DM['Py'][BenchMode][1])])
                    limitX = plt.xlim()
                    plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-caches[ind].DM[SimVar][BenchMode][key].size/expectedNr)*100)))
                    plt.savefig('./histograms/' + result.modelVariant + '/SingleRun/' + f'/CE{SimVar}-{BenchMode}-{key}.pdf')
                    plt.clf()

                    # single DM, local edges
                    plt.hist(caches[ind].DM[SimVar][BenchMode][key], 10, histtype='bar')                    
                    figuretitle = 'DM: ' + result.modelVariant + ' Sim: ' + SimVar + ' BenchToggle: ' + BenchMode + ' Sim #: ' + key
                    plt.title(figuretitle)
                    plt.xlabel(r'Benched time [$\mu$sec]')
                    plt.ylabel("count")
                    meanVal = caches[ind].DM[SimVar][BenchMode][key].mean()
                    plt.axvline(x=meanVal,ls=':', color='purple')
                    limitY = plt.ylim()
                    # print(limitY)
                    plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                    plt.xlim(edges[ind].DM[SimVar][BenchMode])
                    limitX = plt.xlim()
                    plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-caches[ind].DM[SimVar][BenchMode][key].size/expectedNr)*100)))
                    plt.savefig('./histograms/' + result.modelVariant + '/SingleRun/' + f'/{SimVar}-{BenchMode}-{key}.pdf')
                    plt.clf()

                    # single Sim, global edges
                    plt.hist(caches[ind].Sim[SimVar][BenchMode][key], 10, histtype='bar')                    
                    figuretitle =  'Sim: ' + SimVar + 'DM: ' + result.modelVariant + ' BenchToggle: ' + BenchMode + ' Sim #: ' + key
                    plt.title(figuretitle)
                    plt.xlabel(r'Benched time [$\mu$sec]')
                    plt.ylabel("count")
                    meanVal = caches[ind].Sim[SimVar][BenchMode][key].mean()
                    plt.axvline(x=meanVal,ls=':', color='purple')
                    limitY = plt.ylim()
                    plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                    plt.xlim([min(glEDGES.Sim['Cpp'][BenchMode][0],glEDGES.Sim['Py'][BenchMode][0]),max(glEDGES.Sim['Cpp'][BenchMode][1],glEDGES.Sim['Py'][BenchMode][1])])
                    limitX = plt.xlim()
                    plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-caches[ind].Sim[SimVar][BenchMode][key].size/expectedNr)*100)))
                    plt.savefig('./histograms/' + result.modelVariant + '/SingleRun/' + f'/CEEM{SimVar}-{BenchMode}-{key}.pdf')
                    plt.clf()

                    # single DM, local edges
                    plt.hist(caches[ind].Sim[SimVar][BenchMode][key], 10, histtype='bar')                    
                    figuretitle = 'Sim: ' + SimVar + 'DM: ' + result.modelVariant + ' BenchToggle: ' + BenchMode + ' Sim #: ' + key
                    plt.title(figuretitle)
                    plt.xlabel(r'Benched time [$\mu$sec]')
                    plt.ylabel("count")
                    meanVal = caches[ind].Sim[SimVar][BenchMode][key].mean()
                    plt.axvline(x=meanVal,ls=':', color='purple')
                    limitY = plt.ylim()
                    plt.text(meanVal,limitY[1]*0.8," mean = {:.4g}".format(meanVal))
                    plt.xlim(edges[ind].Sim[SimVar][BenchMode])
                    limitX = plt.xlim()
                    plt.text((limitX[1]-limitX[0])*0.6+limitX[0],limitY[1]*0.9,"outlier via IQR: {:.2g}%".format(((1-caches[ind].Sim[SimVar][BenchMode][key].size/expectedNr)*100)))
                    plt.savefig('./histograms/' + result.modelVariant + '/SingleRun/' + f'/EM{SimVar}-{BenchMode}-{key}.pdf')
                    plt.clf()
    print("All tasks finished.")
if __name__ == "__main__":
    main()
                #
                # create histogram of all values collected

