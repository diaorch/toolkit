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
    mappedMean = rankSeries.apply(lambda x: np.mean(meanSeries[(x - 1):(x - 1 + sum(rankSeries == x))]))
    # in anonymous use (x - 1) to adjust for indexing
    return(mappedMean)

def quantileNormalization(inputDf):
    # remove NAs 
    completeDf = inputDf.dropna(axis = 0, how = 'any')
    # rank
    rankDf = completeDf.rank(axis = 0, method = 'min', ascending = True)
    rankDf = rankDf.astype(int) # risky when using some other ranking methods
    # sort
    sortDf = completeDf.copy()
    sortDf = pd.DataFrame(np.sort(sortDf.values, axis = 0), index = sortDf.index, columns = sortDf.columns)
    # calculate mean for assuming no tie ranks
    rowMean = sortDf.mean(axis = 1, skipna = True)
    # map mean values to rank, dealing with ties
    mappedDf = rankDf.apply(lambda x: mapTieRankToMean(x, meanSeries = rowMean))
    
    return(mappedDf)
    
