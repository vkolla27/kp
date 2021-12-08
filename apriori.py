from itertools import chain, combinations
import time
import random

def filterCandidateItems(candidateItemsSet, transactions, minSup):
    filteredCandidates = set()
    candidateItemsList = list(candidateItemsSet)
    
    for candidateItems in candidateItemsList:
        sup = 0
        for transaction in transactions:
            if candidateItems.issubset(transaction):
                sup += 1

        if(sup >= minSup): 
            filteredCandidates.add(candidateItems)

    return filteredCandidates

def impApriori(file, minSup):
    items = set()
    freqItemSets = set()
    transactions = []

    for line in file.readlines():
        transaction = str(line.strip(), 'UTF-8').split(", ")
        key = transaction.pop(0)
        items = items.union(transaction)
        transaction = set([int(x) for x in transaction])
        transaction.add(key+'key')
        transactions.append(frozenset(transaction))

    itemSet = set( frozenset([int(item)]) for item in items)

    start = time.time()
    candidateItemFreqFiltered = filterCandidateItems(itemSet, transactions, minSup)    
    
    for freqItem in candidateItemFreqFiltered:
        freqItemSets.add(freqItem)

    setSize = 2

    while (len(candidateItemFreqFiltered) != 0):    

        candidateItems = set([i.union(j) for i in candidateItemFreqFiltered for j in candidateItemFreqFiltered if len(i.union(j)) == setSize])
        
        updatedCandidates = set()
        for candidate in candidateItems:
            subSets = set([frozenset(list(x)) for x in list(chain.from_iterable(combinations(candidate, r) for r in range(setSize-1, setSize)))])
            areAllItemsFreq =  all(item in freqItemSets for item in subSets)

            if areAllItemsFreq is True:
                updatedCandidates.add(candidate)
                    

        candidateItemFreqFiltered = filterCandidateItems(updatedCandidates,transactions, minSup)
        
        for candidate in candidateItemFreqFiltered:
            subSets = set([frozenset(list(x)) for x in list(chain.from_iterable(combinations(candidate, r) for r in range(setSize-1, setSize)))])
            freqItemSets.add(candidate)
            freqItemSets = freqItemSets - subSets
        
        setSize += 1
         
    end = time.time() 
    
    returnItem = [set(x) for x in freqItemSets]
    return(returnItem , end-start)
