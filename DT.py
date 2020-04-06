import random
import csv
import numpy as np
import pandas as pd

def initializePopulation(n):
    choice = [1,2,3,4]
    population = []
    for i in range (0,n):
        individual = []
        nrule = 1 #random.choice(choice)
        #print(nrule * 15)
        for j in range (nrule*15):
            zeroone = random.randint(0,1)
            individual.append(zeroone)
        population.append(individual)
    return population


def loadCsv(x):
    data = []
    with open(x) as csv_data:
        csv_reader = csv.reader(csv_data)
        for i in csv_reader:
            data.append(i)
        return(data)

def binaryEncode(data):
    dictSuhu = {}
    dictWaktu = {}
    dictLangit = {}
    dictKelembapan = {}
    dictTerbang = {}

    # Adding list as value
    dictSuhu['rendah'] = [0, 0, 1]
    dictSuhu['normal'] = [0, 1, 0]
    dictSuhu['tinggi'] = [1, 0, 0]
    dictWaktu['pagi'] = [0, 0, 0, 1]
    dictWaktu['siang'] = [0, 0, 1, 0]
    dictWaktu['sore'] = [0, 1, 0, 0]
    dictWaktu['malam'] = [1, 0, 0, 0]
    dictLangit['cerah'] = [0, 0, 0, 1]
    dictLangit['berawan'] = [0, 0, 1, 0]
    dictLangit['rintik'] = [0, 1, 0, 0]
    dictLangit['hujan'] = [1, 0, 0, 0]
    dictKelembapan['rendah'] = [0, 0, 1]
    dictKelembapan['normal'] = [0, 1, 0]
    dictKelembapan['tinggi'] = [1, 0, 0]
    dictTerbang['tidak'] = [0]
    dictTerbang['ya'] = [1]

    dataResult = []
    for row in data:
        temp = []
        temp.extend(dictSuhu[row[0]])
        temp.extend(dictWaktu[row[1]])
        temp.extend(dictLangit[row[2]])
        temp.extend(dictKelembapan[row[3]])
        temp.extend(dictTerbang[row[4]])
        dataResult.append(temp)
    return dataResult

def trueOrFalse(i,j):
    logical = np.logical_and(i, j)
    logicalSuhu = np.logical_or(logical[0], np.logical_or(logical[1], logical[2]))
    logicalWaktu = np.logical_or(logical[3], np.logical_or(logical[4], np.logical_or(logical[5], logical[6])))
    logicalLangit = np.logical_or(logical[7], np.logical_or(logical[8], np.logical_or(logical[9], logical[10])))
    logicalKelembapan = np.logical_or(logical[11], np.logical_or(logical[12], logical[13]))
    conclusion = np.logical_and(logicalSuhu,
                                np.logical_and(logicalWaktu, np.logical_and(logicalLangit, logicalKelembapan)))
    return conclusion

def listPair(list,encodedData):
    pairList = []
    for i in list:
        value = fitnessEvaluation(i,encodedData)
        pair = [i,value]
        pairList.append(pair)
    pairList = sorted(pairList, key=lambda tup: tup[1], reverse=True)
    return pairList

def fitnessEvaluation(arr, encodedData):
    hit = 0
    fitnessValue = 0
    div = len(arr)//15
    if (div == 1):
        n = 1
        for j in encodedData:
            if trueOrFalse(arr,j):
                if arr[14] == j[14]:
                    hit = hit + 1
            else:
                if arr[14] != j[14]:
                    hit = hit + 1
        fitnessValue = (hit/80)*100
    #else:
        #Hitung fitness jika panjang kromosom berbeda (belum selesai)
    return fitnessValue

def tournament(initializedPop,encodedData,n_parent,k_idv):
    solution = []
    for i in range(n_parent):
        best = []
        for i in range(k_idv):
            a = (best == [])
            idv = initializedPop[random.randint(0, len(initializedPop) - 1)]
            if (best == []):
                best = idv
            else:
                fit_idv = fitnessEvaluation(idv,encodedData)
                fit_best = fitnessEvaluation(best,encodedData)
                if (fit_idv > fit_best):
                    best = idv
        solution.append(best)
    return solution

def crossover(solution):
    offspring = []
    P1 = []
    P2 = []
    crossoverProb = 70 / 100
    rng = random.uniform(0, 1)
    if(rng <= crossoverProb):
        if(len(solution[0])>len(solution[1])):
            P1 = solution[1]
            P2 = solution[0]
        else:
            P1 = solution[0]
            P2 = solution[1]
        splitStartSP1 = random.randint(1, (len(P1)//2-2))
        splitEndSP1 = random.randint((len(P1)//2+2), len(P1)-2)
        if splitStartSP1 > splitEndSP1:
            splitStartSP1, splitEndSP1 = splitEndSP1, splitStartSP1
        n_gen = splitEndSP1 - splitStartSP1
        gap = n_gen % 15
        if (n_gen == gap):
            splitStartSP2 = splitStartSP1
            splitEndSP2 = splitEndSP1
            offspring1 = P1[:splitStartSP1] + P2[splitStartSP2:splitEndSP2] + P1[splitEndSP1:]
            offspring2 = P2[:splitStartSP2] + P1[splitStartSP2:splitEndSP2] + P2[splitEndSP2:]
            offspring.append(offspring1)
            offspring.append(offspring2)
        else:
            #Crossover jika panjang kromosom P1 dan P2 berbeda (belum selesai)
            choice = [[splitStartSP1,(splitStartSP1+n_gen)],[splitStartSP1,(splitStartSP1+gap)],[(splitEndSP1-n_gen),splitEndSP1],[(splitEndSP1-gap),splitEndSP1]]
            splitSP2 = random.randint(choice)
    else:
        offspring = solution
    return offspring

def mutation(offspring):
    mutatedoffs = []
    mutationProb = 0.1
    for i in offspring:
        rng = random.uniform(0, 1)
        #print(rng)
        if (rng < mutationProb):
            randIndex = random.randint(0, len(i) - 1)
            if (i[randIndex] == 0):
                i[randIndex] = 1
            elif (i[randIndex] == 1):
                i[randIndex] = 0
            mutatedoffs.append(i)
        else:
            mutatedoffs.append(i)
    return mutatedoffs

def steadyState(initializedPop,mutatedoffs,encodedData):
    fitnessPop = listPair(initializedPop,encodedData)
    fitnessOffs = listPair(mutatedoffs,encodedData)
    arrPairNextGen = []
    arrNextGen = []
    for i in fitnessPop:
        arrPairNextGen.append(i)
    seconde_lastArr = len(fitnessPop)-2
    for i in fitnessOffs:
        if (i[1] > fitnessPop[seconde_lastArr][1]) or (i[1] == fitnessPop[seconde_lastArr][1]):
            arrPairNextGen[seconde_lastArr] = i
        seconde_lastArr = seconde_lastArr + 1
    arrPairNextGen = sorted(arrPairNextGen, key=lambda tup: tup[1], reverse=True)
    for i in arrPairNextGen:
        arrNextGen.append(i[0])
        #print(i)
    #for j in arrNextGen:
        #print(j)
    #print('\n')
    return arrNextGen

def valueDataUji(kromosomTerbaik,load2):
    arrHasilUji = []
    dictSuhu = {}
    dictWaktu = {}
    dictLangit = {}
    dictKelembapan = {}

    # Adding list as value
    dictSuhu['Rendah'] = [0, 0, 1]
    dictSuhu['Normal'] = [0, 1, 0]
    dictSuhu['Tinggi'] = [1, 0, 0]
    dictWaktu['Pagi'] = [0, 0, 0, 1]
    dictWaktu['Siang'] = [0, 0, 1, 0]
    dictWaktu['Sore'] = [0, 1, 0, 0]
    dictWaktu['Malam'] = [1, 0, 0, 0]
    dictLangit['Cerah'] = [0, 0, 0, 1]
    dictLangit['Berawan'] = [0, 0, 1, 0]
    dictLangit['Rintik'] = [0, 1, 0, 0]
    dictLangit['Hujan'] = [1, 0, 0, 0]
    dictKelembapan['Rendah'] = [0, 0, 1]
    dictKelembapan['Normal'] = [0, 1, 0]
    dictKelembapan['Tinggi'] = [1, 0, 0]

    dataResult = []
    for row in load2:
        temp = []
        temp.extend(dictSuhu[row[0]])
        temp.extend(dictWaktu[row[1]])
        temp.extend(dictLangit[row[2]])
        temp.extend(dictKelembapan[row[3]])
        dataResult.append(temp)

    for j in dataResult:
        if (trueOrFalse(kromosomTerbaik[:14],j)):
            arrHasilUji.append('ya')
        else:
            arrHasilUji.append('tidak')
    return arrHasilUji

def writeCsv(hasil):
    resultCsv = []
    fields = ['Terbang/tidak']
    for i in hasil:
        resultCsv.append([i])
    print(resultCsv)
    filename = "resultCsv.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(resultCsv)

def run(n):
    initializedPop = initializePopulation(10)
    load = loadCsv('data_latih_opsi_1.csv')
    encodedData = binaryEncode(load)
    for i in range (n):
        #print("Generasi ke-",i+1)
        parentSelection = tournament(initializedPop,encodedData,2,4)
        cross = crossover(parentSelection)
        mutate = mutation(cross)
        generationReplacement = steadyState(initializedPop,mutate,encodedData)
        initializedPop = generationReplacement
    kromosomTerbaik = initializedPop[0]
    print('Kromosom terbaik dari '+ str(n) +' generasi : ',kromosomTerbaik)
    load2 = loadCsv('data_uji_opsi_1.csv')
    hasil = valueDataUji(kromosomTerbaik,load2)
    writeCsv(hasil)

n = int(input("Masukkan jumlah generasi : "))
run(n)