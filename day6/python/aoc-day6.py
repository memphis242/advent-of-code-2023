#################### ---IMPORTS--- #################### 
from typing import Tuple, List
import sys
import time
from datetime import timedelta
import math

#################### --CONSTANTS-- #################### 
# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day6/python/day6-puzzle-input.txt'
TEST_INPUT = 'C:/git/aoc/advent-of-code-2023/day6/python/day6-test-input.txt'
FILE_INPUT = TEST_INPUT

#################### --FUNCTIONS-- #################### 
def get_next_num_in_line_starting_at_idx( line: str, start_idx: int ) -> Tuple[str, int]:
   # check for invalid start index
   if start_idx > (len(line)-1):
      return ('', 0)

   chars_to_skip_over_afterwards = 0
   num_str = ''
   for char_idx,char in enumerate(line[start_idx:]):

      # skip over non-digits and increment chars to skip
      if not char.isdigit():
         chars_to_skip_over_afterwards = chars_to_skip_over_afterwards + 1
         continue

      # iterate through digits until non-digit is found
      num_str = char
      check_idx = start_idx + char_idx + 1
      if check_idx <= len(line)-1:
         check_char = line[check_idx]
      else:
         check_char = ''
      while check_char.isdigit():
         num_str = num_str + check_char
         check_idx = check_idx + 1
         if check_idx <= len(line)-1:
            check_char = line[check_idx]
         else:
            break
      chars_to_skip_over_afterwards = chars_to_skip_over_afterwards + len(num_str) - 1
      
      # num found, stop iteration over line
      break

   return ( num_str, chars_to_skip_over_afterwards )

def get_mapping_triple( line: str ) -> Tuple[int, int, int]:
   num_list = []
   loop_skip_counter = 0
   for char_idx, char in enumerate(line):
      # skip over characters if applicable
      if loop_skip_counter > 0:
         loop_skip_counter -= 1
         continue

      # skip over non-digits and increment chars to skip
      if not char.isdigit():
         continue

      # iterate through digits until non-digit is found
      num_str = char
      check_idx = char_idx + 1
      if check_idx <= len(line)-1:
         check_char = line[check_idx]
      else:
         check_char = ''
      while check_char.isdigit():
         num_str = num_str + check_char
         check_idx = check_idx + 1
         if check_idx <= len(line)-1:
            check_char = line[check_idx]
         else:
            break
      
      # num found, assign to triple
      loop_skip_counter = len(num_str) - 1
      num_list.append(int(num_str))
      # check if we've filled up the triple already
      if len(num_list) >= 3:
         break

   return ( num_list[0], num_list[1], num_list[2] )

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    # print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    # Print New Line on Complete
    if iteration == total: 
        print()
#################### ----MAIN----- #################### 
# strategy: traverse directly from seed to location without creating every mapping first

program_start_time = time.time()

if len(sys.argv) < 2:
   file_to_search = FILE_INPUT
   # file_to_search = SUB_PUZZLE_INPUT
elif sys.argv[1] == '0':
   file_to_search = TEST_INPUT
elif sys.argv[1] == '1':
   file_to_search = PUZZLE_INPUT
else:
   # TODO:
   file_to_search = TEST_INPUT
with open(file_to_search, 'r') as puzzle_input:
# with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

# this is a pretty easy kinematics/basic algebra problem.
# - we know the basic uniform acceleration relationship between change-in-position vs uniform acceleration: dx = (vi x dt) + ( 0.5 x a x dt^2 )
# - as well as the relationship between change-in-position vs an average velocity: dx = v x dt
# - we know that dt = (total race time) - (time holding button down) = T - td
# - also, while holding the button, we increase our v while driving by 1 (mm/s)/s
# and we are solving for dx > x_record, in the integer set
# also we don't even have to worry about the quadratic since while holding the button down, we aren't moving. so it's really just the dx(v) equation.
# given an x_record, v x dt > x_record ==> v x (T - td) > x_record ==> ( td ) x (T - td) > x_record ==> -td^2 + T*td > x_record ==> -td^2 + T*td - x_record > 0 ==> td^2 - T*td + x_record < 0
# okay! we want to know **where the quadratic td^2 - T*td + x_record is below 0**, if applicable.
# we know every quadratic has two roots. either:
# A- both roots are zero ==> in which case, we have no solution since our curve is concave up
# B- both roots are imaginary ==> in which case, we again have no solution since our curve is totally above the x-axis
# C- both roots are non-zero ==> in which case the solution lies in between the roots!
# also, to find the roots, we go back to our classic algebra **quadratic formula**, which applied here would be:
# td_roots = (1/2) * ( T +- sqrt( T^2 - 4*x_record ) ) ==> (T/2) +- sqrt(T^2 - 4*x_record)/2
# and since we know our quadratic is concave down, we'll want to round up the lower root and round down the upper root

TIME_ROW = 0
DISTANCE_ROW = 1
max_times = []
record_distances = []
loop_skip_counter = 0

# max times
for char_idx, char in enumerate( puzzle_input_lines[TIME_ROW] ):
   # skip characters if applicable
   if loop_skip_counter > 0:
      loop_skip_counter -= 1
      continue
   ( max_time, loop_skip_counter ) = get_next_num_in_line_starting_at_idx( puzzle_input_lines[TIME_ROW], char_idx )
   if max_time == '':
      continue
   max_times.append(int(max_time))

# record distances
loop_skip_counter = 0
for char_idx, char in enumerate( puzzle_input_lines[DISTANCE_ROW] ):
   # skip characters if applicable
   if loop_skip_counter > 0:
      loop_skip_counter -= 1
      continue
   ( distance, loop_skip_counter ) = get_next_num_in_line_starting_at_idx( puzzle_input_lines[DISTANCE_ROW], char_idx )
   if distance == '':
      continue
   record_distances.append(int(distance))

# find number of possiblities!
num_of_possibilities = []
for idx,max_time in enumerate( max_times ):
   # find roots of quadratic formed
   to_be_sqrt = max_time*max_time - 4*record_distances[idx]
   if to_be_sqrt < 0:
      num_of_possibilities.append(0)
      continue
   num_sqrt = math.sqrt(to_be_sqrt)
   root_upper = (max_time + num_sqrt)/2
   root_lower = (max_time - num_sqrt)/2
   if int(root_upper) == root_upper:
      range_upper = int(root_upper) - 1
   else:
      range_upper = int(root_upper)
   if int(root_lower) == root_lower:
      range_lower = int(root_lower) + 1
   else:
      range_lower = int(root_lower + 1)
   num_of_possibilities.append( range_upper - range_lower + 1 )

# multiply them all up for the answer submission
product_of_possiblities = 1
for possibility in num_of_possibilities:
   product_of_possiblities *= possibility

print(f'\n\nPart 1:\tProduct of Possibilities: {product_of_possiblities}')
print(f'Part 2:\t')

program_end_time = time.time()
total_program_time = program_end_time - program_start_time
total_program_time_hh_mm_ss = str(timedelta( seconds=total_program_time ))
hh_mm_ss = total_program_time_hh_mm_ss.split(':')
print(f'\nTotal Program Execution Time: {hh_mm_ss[0]}h {hh_mm_ss[1]}m {hh_mm_ss[2]}s')