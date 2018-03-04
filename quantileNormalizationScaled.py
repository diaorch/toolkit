#!/use/bin/env python2

"""
quantile normalize a numeric data frame
with ties treated as pooled average of all values corresponding quantiles

Special thanks to StackOverflow post: 
https://stackoverflow.com/questions/37935920/quantile-normalization-on-pandas-dataframe
https://stackoverflow.com/questions/43280322/sort-all-columns-of-a-pandas-dataframe-independently-using-sort-values
"""
import numpy as np
import pandas as pd

def mapTieRankToMean(rankSeries, meanSeries):
    """
    map ranks to mean dealing with ties, in one loop of N (or length(ranks))
    """
    # sort index series
    rankSort = np.sort(rankSeries)
    meanSort = np.sort(meanSeries)
    # calculate the mean for each rank
    prevIndex = 0
    currentIndex = 0
    rankRecord = []
    meanRecord = []
    
    while(currentIndex < len(rankSeries)):
        prevRank = rankSort[prevIndex]
        currentRank = rankSort[currentIndex]
        if (currentRank == prevRank):
            rankRecord.extend([meanSort[currentIndex]])
            currentIndex += 1
        else:
            rankMean = np.mean(rankRecord)
            rankRecord = []
            meanRecord.extend([rankMean] * (currentIndex - prevIndex))
            prevIndex = currentIndex
    rankMean = np.mean(rankRecord)
    meanRecord.extend([rankMean] * (currentIndex - prevIndex))
    
    mappedMean = pd.Series(meanRecord)[np.array(rankSeries) - 1]
    mappedMean.index = rankSeries.index
    return(mappedMean)

def quantileNormalization(inputDf):
    # find NAs for error
    if (inputDf.isnull().values.any()):
        raise ValueError('Input dataframe contains NaN')
    # rank
    rankDf = inputDf.rank(axis = 0, method = 'min', ascending = True)
    rankDf = rankDf.astype(int) # risky when using some other ranking methods
    # print(rankDf)
    # sort
    sortDf = inputDf.copy()
    sortDf = pd.DataFrame(np.sort(sortDf.values, axis = 0), index = sortDf.index, columns = sortDf.columns)
    # calculate mean for assuming no tie ranks
    rowMean = sortDf.mean(axis = 1, skipna = True)
    # print(rowMean)
    # map mean values to rank, dealing with ties
    mappedDf = rankDf.apply(func = lambda x: mapTieRankToMean(rankSeries = x, meanSeries = rowMean), axis = 0)
    # print(rankDf.iloc[:, 0])
    # mappedDf = mapTieRankToMean(rankSeries = rankDf.iloc[:, 0], meanSeries = rowMean)
    # print(mappedDf)
    
    return(mappedDf)

