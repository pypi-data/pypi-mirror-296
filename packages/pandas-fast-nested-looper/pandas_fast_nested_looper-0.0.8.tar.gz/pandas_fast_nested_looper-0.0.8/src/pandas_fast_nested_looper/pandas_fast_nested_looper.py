#----------------------------- begining --------------------------------------------------
from tqdm import tqdm
import pandas as pd 
import numpy as np 
from numba import jit
import numba
import time 
import matplotlib.pyplot as plt
from numba_progress import ProgressBar

start_time = time.time()

#----------------------------- main loop --------------------------------------------------
@numba.jit(nogil=True)
def looper(file1_num_iterations, file2_num_iterations, file2_column_A_numpy, file1_column_A_numpy, file1_column_B_numpy, progress):
    file2_column_B_list = [0] * file2_num_iterations

    
    print("\nloop starting...")
    
    for i in range(file2_num_iterations):
        progress[0].update()

        for j in range(file1_num_iterations):
            if file2_column_A_numpy[i] == file1_column_A_numpy[j]:
                
                file2_column_B_list[i] = file1_column_B_numpy[j]

                #print("yes match: ", file2_column_A_numpy[i], file1_column_A_numpy[j])

            else:
                #print("compare : ", file2_column_A_numpy[i], file1_column_A_numpy[j])
                pass
                #file2_column_B_list[i] = 99999999

            progress[1].update(1)
            
        # reset the second progress bar to 0
        progress[1].set(0)
        # print(i)

    
    
    return file2_column_B_list


#----------------------------- main function --------------------------------------------------
def pandas_fast_nested_looper(file1_name,file1_column_A, file1_column_B, file2_name, file2_column_A, file2_new_column_name):
    
    # loading files ----------------------------------------------
    print('loading file1 ......')
    file1_df = pd.read_csv(file1_name) #, index_col="__newID
    file1_columns = list(file1_df)
    print(file1_columns)

    print('loading file2 ......')
    file2_df = pd.read_csv(file2_name) #, index_col="__newID
    file2_columns = list(file2_df)
    print(file2_columns)

    #type changing and numpy --------------------------------------
    #change dtype to int
    file1_df[file1_column_A] = file1_df[file1_column_A].astype(int)
    file1_df[file1_column_B] = file1_df[file1_column_B].astype(int)
    file2_df[file2_column_A] = file2_df[file2_column_A].astype(int)

    #convert pandas columns to numpy-------------------------------
    file1_column_A_numpy = file1_df[file1_column_A].to_numpy()
    file1_column_B_numpy = file1_df[file1_column_B].to_numpy()
    file2_column_A_numpy = file2_df[file2_column_A].to_numpy()

    #count iteration count-----------------------------------------
    file1_num_iterations  = file1_column_A_numpy.shape[0]
    file2_num_iterations = file2_column_A_numpy.shape[0]

    print('file1_num_iterations: ', file1_num_iterations)
    print('file2_num_iterations: ', file2_num_iterations)
    print('total iterations: ', file1_num_iterations*file2_num_iterations)

    with ProgressBar(total=file2_num_iterations, ncols=80) as numba_progress1, ProgressBar(total=file1_num_iterations, ncols=80) as numba_progress2:
        file2_column_B_list = looper(file1_num_iterations, file2_num_iterations, file2_column_A_numpy, file1_column_A_numpy, file1_column_B_numpy, (numba_progress1, numba_progress2))

    #append new column
    file2_df[file2_new_column_name] = file2_column_B_list

    print("saving file1 with new column to disk ....")
    file2_df.to_csv("df2_with_new_column.csv")

    #print("\n", file2_column_B_list, "\n done!")
    print('start calucating total loop time... ')
    end_time = time.time()
    print('\nDone! Elapsed time: {} seconds'.format((end_time - start_time)))

    return file2_column_B_list, file2_df



#----------------------------- test --------------------------------------------------
file1_name = "age_added.csv"
file2_name = "subscriber.csv"

file1_column_A = 'id_billing_user'
file1_column_B = '__newID'

file2_column_A = 'user_id'

file2_new_column_name = "all_user_id"

#function test
#file2_column_B_list, file2_df = pandas_fast_nested_looper(file1_name, file1_column_A, file1_column_B, file2_name, file2_column_A, file2_new_column_name)

