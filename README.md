# Modified-Cellular-Life-Simulator
Program uses Python to create a modified cellular life simulator
--------------------------------------------------------------------------------------------------------------------
This Python program is capable of executing the first 100 steps of a modified cellular life
simulator. The simulator will receive the path to the input file as an argument containing the starting cellular
matrix. The program will then simulate the next 100 time-step. The simulation is guided by a handful of simplistic 
rules that will result in a seemingly complex simulation of cellular organisms.

Below is an example starting cellular matrix consisting of 10 rows and 20 columns:

['-----+--+-+----+----\n', 
'---++-----+-----+---\n', 
'-------++---+--++---\n', 
'+--------++++---++++\n', 
'+----++--+--++--++++\n', 
'+------+----+--+---+\n', 
'+-------------++---+\n', 
'+----------+--+----+\n', 
'-+--------------+---\n', 
'----+-++-------+---+]

The program will accept the starting matrix (Time Step 0) as a file from the command line and then simulate
steps 1 through 100. The program will also accept a number of threads to be used from a seperate command line argument.
The final matrix (Time Step 100) will then be written to an output file whose name and
path is dictated by a separate command line argument. These files will contain a copy of the matrix with each
row of the matrix printed on separate lines and no characters in between the columns.

Example executions:
• python3 MCL_Simulator.py -i inputFile.txt -o timeStep100.txt -t 36
  o Sets input file to “inputFile.txt”
  o Sets output file to “timeStep100.txt”
  o Sets thread count to 36

Valid input and output files must abide by the following rules:
1) The matrix may only contain the following symbols:
  a. Hyphens ‘-’ to signify currently “dead” cells.
  b. Plus signs ‘+’ to signify currently “alive” cells.
  c. End of Line Characters marking the end of each row.
2) The matrix may not contain any spaces, commas, or other delimiters between symbols.
3) The matrix must separate rows with a line break.
4) The final row does not require a line break but may include one.
5) Files containing any other symbols beyond those listed in #1 are considered invalid.

Using this starting cellular matrix, the program will then simulate the next 100 steps of a simulation that
uses the following rules to dictate what occurs during each time step:
  1) Any position in the matrix with a hyphen ‘-’ is considered “dead” during the current time step.
  2) Any position in the matrix with a plus sign ‘+’ is considered “alive” during the current time step.
  3) If an “alive” square has two, four, or six living neighbors, then it will be “alive” in the next time step.
  4) If a “dead” square has a prime number of living neighbors, then it continues to be “alive” in the next
     time step.
  5) Every other square dies or remains dead, causing it to be “dead” in the next time step.
  
For this program, a neighbor is defined as any cell that touches the current cell, meaning each current cell,
regardless of position, has 8 neighboring cells. Cells located at the edge should “wrap around” the matrix to find
their other neighbors.
