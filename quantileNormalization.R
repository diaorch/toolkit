# USAGE:
# Rscript quantileNormalization.R --input=~/data/ss/ss-qNormReplicates.test.csv --output=~/data/ss/ss-qNormReplicates.test.RNormed.csv --start=2

normalizeByQuantiles <- function(M, ties = TRUE){
  # not roboust for NAs?
  sampleNames <- colnames(M)
  M <- M[complete.cases(M), ]
  # M is a numeric matrix
  if (is.vector(M)){
    M <- as.matrix(M, ncol = 1)
    colnames(M) <- sampleNames
  }
  
  rankedM <- apply(X = M, MARGIN = 2, FUN = rank, ties.method = 'min')
  print('ranked')
  sortedM <- apply(X = M, MARGIN = 2, FUN = sort)
  print('sorted')
  if (!ties){
    meanRowM <- apply(X = sortedM, MARGIN = 1, FUN = mean)
    # function to retrive individual means from index
    convertIndexToMean <- function(index, meanVector)(
      return(meanVector[index])
    )
    mappedMeanM <- apply(X = rankedM, MARGIN = 2, convertIndexToMean, meanVector = meanRowM)
  } else{
    calcMeanWithTies <- function(indivRank, rankVec, sortedMtx){
      rankIdx <- sum(rankVec == indivRank)
      rankStart <- indivRank
      rankEnd <- rankStart + rankIdx - 1
      allValue <- as.vector(sortedMtx[rankStart:rankEnd, ])
      return(mean(allValue))
    }
    mapMeanToVector <- function(rankVec, sortedMtx){
      print(head(rankVec))
      meanWithTiesVector <- sapply(X = rankVec, FUN = calcMeanWithTies, 
                                   rankVec = rankVec, sortedMtx = sortedMtx)
      return(meanWithTiesVector)
    }
    mappedMeanM <- apply(X = rankedM, MARGIN = 2, FUN = mapMeanToVector, 
                         sortedMtx = sortedM)
    print('mapped')
  }
  return(mappedMeanM)
}

### take args from command line
args <- commandArgs(TRUE)

## rarse arguments (we expect the form --arg=value)
parseArgs <- function(x) strsplit(sub("^--", "", x), "=")
argsDF <- as.data.frame(do.call("rbind", parseArgs(args)))

## arguments
inputFilename <- as.character(argsDF$V2[argsDF$V1 == 'input'])
outputFilename <- as.character(argsDF$V2[argsDF$V1 == 'output'])
startColumn <- as.character(argsDF$V2[argsDF$V1 == 'start'])
startColumn <- as.numeric(startColumn)

## read file
inputDf <- read.csv(file = inputFilename, header = FALSE)

print(head(inputDf))
startColumn

## subset matrix
supplColumns <- inputDf[, 1:(startColumn - 1)]
normColumns <- inputDf[, startColumn:ncol(inputDf)]

print("subsetted")
print(head(normColumns))

## quantile normalize
qNormedColumns <- normalizeByQuantiles(M = normColumns, ties = TRUE)

print("normalized")

## bind supplementary information and normalized matrix
if (!is.null(supplColumns)){
  outputDf <- as.data.frame(cbind(supplColumns, qNormedColumns))
} else{
  outputDf <- as.data.frame(qNormedColumns)
}

# print csv to screen
print(head(outputDf))
write.table(outputDf, file = outputFilename, sep = ',', row.names = FALSE, col.names = FALSE, quote = FALSE)

