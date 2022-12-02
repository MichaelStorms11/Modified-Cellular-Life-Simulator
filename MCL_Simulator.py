import copy
import argparse
from multiprocessing import Pool
from math import floor
def process(threads):   # Function that processes are mapped to.
    even = [2,4,6]      # List of even numbers to compare neighbors to.
    prime = [2,3,5,7]   # List of prime numbers to compare neighbors to.
    newMatrix = copy.deepcopy(threads)          # Copy input matrix.
    for x in range(len(threads)):
        row = list(threads[x])                  # Create list of input line from string.
        for y in range(len(row)):               # Iterate through matrix columns.
                neighbors = 0                   # Count of neighbors set to 0.
                if x < len(threads) and threads[x - 1][y] == '+':        # check for above neighbor.
                    neighbors += 1
                if y < len(row) and threads[x][y - 1] == '+':            # Check for left neighbor.
                    neighbors += 1
                if x < len(threads) and y < len(row) and threads[x - 1][y - 1] == '+':  # Check For top left neighbor.
                    neighbors += 1
                if x < len(threads) - 1 and threads[x + 1][y] == '+':                   # Check for below neighbor.
                    neighbors += 1
                elif x == len(threads) - 1 and threads[0][y] == '+':                    # Check for below wrapped neighbor.
                    neighbors += 1
                if y < len(row) - 1 and threads[x][y + 1] == '+':                       # Check for right neighbor.
                    neighbors += 1
                elif y == len(row) - 1 and threads[x][0] == '+':                        # Check for right wrapped neighbor.
                    neighbors += 1
                if x < len(threads) - 1 and y < len(row) - 1 and threads[x + 1][y + 1] == '+':      # Check for bottom right neighbor.
                    neighbors += 1
                elif x < len(threads) - 1 and y == len(row) - 1 and threads[x+1][0] == '+':         # Check for bottom right neighbor on right side of matrix.
                    neighbors += 1
                elif x == len(threads) - 1 and y < len(row) - 1 and threads[0][y + 1] == '+':       # Check for bottom right wrapped neighbor on bottom side of matrix.
                    neighbors += 1
                elif x == len(threads) - 1 and y == len(row) - 1 and threads[0][0] == '+':          # Check for bottom right wrapped neighbor in bottom right corner.
                    neighbors += 1
                if x < len(threads) - 1 and y < len(row) and threads[x + 1][y - 1] == '+':          # Check for Bottom left neighbor.
                    neighbors += 1
                elif x == len(threads) - 1 and y < len(row) and threads[0][y - 1] == '+':           # Check for bottom left wrapped neighbor on bottom of matrix.
                    neighbors += 1
                if x < len(threads) and y < len(row) - 1 and threads[x - 1][y + 1] == '+':          # Check for top right neighbor.
                    neighbors += 1
                elif x < len(threads) and y == len(row) - 1 and threads[x - 1][0] == '+':           # Check for top right neighbor on right side of matrix.
                    neighbors += 1
                if '+' in threads[x][y]:    # Case to change live cell depending on neighbors.
                    if neighbors in even:
                        row[y] = '+'
                    else:
                        row[y] = '-'
                elif '-' in threads[x][y]:  # Case to change dead cell depending on neighbors.
                    if neighbors in prime:
                        row[y] = '+'
                    else:
                        row[y] = '-'
        temp = ''.join(row) # Combine list into string.
        newMatrix[x] = temp # Assign new string to temp matrix.
    realResults = []
    for z in range(len(newMatrix)):         # Doesn't append boundaries for row above and row below the matrix being edited.
        if(z > 0 and z < len(newMatrix)-1):
            realResults.append(newMatrix[z])
    return realResults

def splitMatrix(inputMatrix, bounds):
    topBounds = [bounds[i][0] for i in range(len(bounds))]      # Unpack bounds data to list of top bounds.
    bottomBounds = [bounds[i][1] for i in range(len(bounds))]   # Unpack the bounds data to a list of bottom bounds.
    rowsByBounds = []
    if (args.threads > 1):  # Case for if threads are greater than 1.
        for x in range(args.threads):   # Runs for the amount of threads given.
            line = []                   # Creates blank array for submatrices.  
            if(bottomBounds[x] != 0):   # Works on everthread but last because bottom bounds == the first line.
                for y in range(floor(len(inputMatrix)/args.threads)+2): # Run for amount of lines per thread plus the row above and below.
                    if(topBounds[x] == len(inputMatrix)-1):             # Case for top bounds equal to last row of the matrix.
                        if y == 0:                                      # Case to add top bound for the case above the first line to edit for thread [0].
                            line.append(inputMatrix[topBounds[x]])      # Append last line of the matrix.
                        else:                       
                            line.append(inputMatrix[y-1])               # Append every other line of the matrix in the thread.
                    else:
                        line.append(inputMatrix[topBounds[x]+y])        # Case for every thread but the first and last threads, appends lines from the matrix starting at the upper bound and iterating to the lower bound
                rowsByBounds.append(line)                               # Appends each line to the matrix to be returned.
            else:                                                       # Case for last row of the matrix.
                for y in range(len(inputMatrix)-topBounds[x]):          # Run for amound of lines per thread expluding the row below.
                    line.append(inputMatrix[topBounds[x]+y])            # Add each line except last.
                line.append(inputMatrix[0])                             # Adds the final bottom bound for the last line of the matrix.
                rowsByBounds.append(line)
    else:                                                               # Case for 1 thread.
        rowsByBounds.append(inputMatrix[len(inputMatrix)-1])            # Add the top bounds for first line in matrix.
        for i in range(len(inputMatrix)):                               # Case for all lines being edited.
            rowsByBounds.append(inputMatrix[i])                         
        rowsByBounds.append(inputMatrix[0])                             # Add the first row of the matrix as bottom bound for last line of the matrix.
        rowsByBounds = [rowsByBounds]                                   # Create a list of list to return.
    return rowsByBounds

def sBounds(poolData):  # Function takes in the rows and indexes of matrix returning a list of tuples of bounds for each thread.
    rows = [poolData[i][0] for i in range(len(poolData))]   # Unpack poolData rows.
    index = [poolData[i][1] for i in range(len(poolData))]  # Unpack poolData indices.
    rowPerThread = floor(len(rows)/args.threads)            # Determine max amount of rows per thread.
    tBounds = []                                            # List of tuples of calculated bounds.
    for i in range(args.threads):                           # Calculate and set row above and row below for row being edited.
        rowAbove = (index[i*rowPerThread-1])
        if i == args.threads-1:
            rowBelow = index[0]
        else:
            rowBelow = (index[(i+1)*rowPerThread])
        for x in range(args.threads):
            ends = [rowAbove,rowBelow]                      # Creates tuple to be added to tBounds.
        tBounds.append(ends)
    return tBounds

def predictMatrix(inputMatrix):
    N = 100               # number of steps to run.
    poolData = []       # Data sent to be split to find bounds.
    for rowNumber in range(len(inputMatrix)):
        row = list(inputMatrix[rowNumber])  # Assign each row of the Matrix.
        processInput = [row, rowNumber]     # Pack each matrixData.
        poolData.append(processInput)   # Assign row and row number to pool data list.
    bounds = sBounds(poolData)  # bounds variable is set to list of tuple of bounds.

    while N:                                  # While steps remain to process.
        splitMatrices = splitMatrix(inputMatrix, bounds)
        processPool = Pool(processes=args.threads)
        results = processPool.map(process, splitMatrices)
        inputMatrix = [item for sublist in results for item in sublist] # Flattens the result list of list into a single list.
        N -= 1  # subtract the step.  
    fo.write("\n".join(item for item in inputMatrix))   # writes each line of the matrix to the output file.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest ='input', type = str, required = True)   # Argparse arguments to take in the input file, output file, and thread count.
    parser.add_argument('-o', dest = 'output', type = str, required = True)
    parser.add_argument('-t', dest = 'threads', type = int, default = 1)
    args = parser.parse_args()
    f = open(args.input, 'r')   # Open given input file.
    fo = open(args.output, 'w') # Open given output file.
    matrix = [line.strip() for line in f.readlines() if line.strip()]  # Store each line that is not an empty string.
    predictMatrix(matrix)
    f.close()
    fo.close()
    
