
# coding: utf-8

# In[ ]:


import numpy as np
from collections import defaultdict


# In[ ]:


sudoku = np.array(
[[5, 1, 7, 6, 0, 0, 0, 3, 4],
 [2, 8, 9, 0, 0, 4, 0, 0, 0],
 [3, 4, 6, 2, 0, 5, 0, 9, 0],
 [6, 0, 2, 0, 0, 0, 0, 1, 0],
 [0, 3, 8, 0, 0, 6, 0, 4, 7],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 9, 0, 0, 0, 0, 0, 7, 8],
 [7, 0, 3, 4, 0, 0, 5, 6, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0]]).reshape((9,9))


# In[ ]:


def solve_sudoku(sudoku, solve_multisolution: bool = False):
    '''Takes sudoku 9x9 array and solves zeros to numbers from 1 to 9. *Only works for 01 solution sudokus.'''
    sudoku = np.array(sudoku, dtype = np.int).reshape((9, 9))
    def subgrid(i, j) -> np.ndarray:
        ''' Take cell's coordinates and then slices respective subgrid.'''
        i, j = np.floor(np.divide((i, j), 3)).astype(int)
        return sudoku[i*3:(i+1)*3,j*3:(j+1)*3]
    iteration_count = 0
    print("Solving sudoku... (0 to 8 x 0 to 8) = 9x9", "\n", sudoku)
    while(True):
        notes = defaultdict(set) #all possible solutions for one given cell
        if iteration_count == 0:
            cells = tuple(zip(*np.where(sudoku!=-1))) #check all cells
        else:
            cells = tuple(zip(*np.where(sudoku==0))) #refresh to check only the zeros to decrease needed computations
        for (i, j) in cells:
            iunique, icounts = np.unique(sudoku[ i, :], return_counts=True)
            junique, jcounts = np.unique(sudoku[ :, j], return_counts=True)
            gunique, gcounts = np.unique(subgrid(i, j), return_counts=True) #g=grid
            if iteration_count == 0:
                if (np.any(icounts[1:]>1) or np.any(jcounts[1:]>1) or np.any(gcounts[1:]>1)): #[1:] excludes the zero(0) count
                    print("Invalid sudoku! Repeating value found near ({}, {})...".format(i, j))
                    return {'solved': False, 'result': sudoku, 'notes': notes}
            if sudoku[i,j] == 0:
                valids = set(range(1, 9+1)) - set().union(iunique).union(junique).union(gunique)
                if len(valids) == 0:
                    print("Invalid sudoku! Unsolvable cell found ({}, {})...".format(i, j))
                    return {'solved': False, 'result': sudoku, 'notes': notes}
                elif len(valids) > 0:
                    for valid in valids: notes[(i, j)].add(valid)
        solved_count = 0
        for (i, j) in list(t for t in notes.keys() if len(notes[t]) == 1):
            sudoku[(i, j)] = list(notes.pop((i, j)))[0]
            solved_count += 1
        iteration_count += 1
        if notes != {} or np.any(sudoku == 0):
            if solved_count == 0:
                print("Unsolvable/multisolution sudoku!")
                print(sudoku, "\n", "Notes: {}".format(notes))
                if solve_multisolution == False:
                    return {'solved': False, 'result': sudoku, 'notes': notes}
                else:
                    print("Making up a solution...")
                    raise Exception("Oh... There's no code to solve it here :(")
            print("Iteration no. {} completed. (Solved {} cells!)".format(iteration_count, solved_count))
        else:
            print("Solved!")
            print(sudoku)
            return {'solved': True, 'result': sudoku, 'notes': notes}

