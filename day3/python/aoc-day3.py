#################### ---IMPORTS--- #################### 
from typing import Tuple, List


# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day3/python/day3-puzzle-input.txt'

#################### --CONSTANTS-- #################### 


#################### --FUNCTIONS-- #################### 
def get_next_num_in_line_starting_at_idx( line: str, start_idx: int ) -> Tuple[str, int]:
   # check for invalid start index
   if start_idx > (len(line)-1):
      return ''

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

def get_adjacency_list( line_list: list, start_idx: int, num_of_digits: int ) -> list:
   adjacency_list = []
   # iterate row-by-row
   for row in line_list:
      if not row: # if row is empty (i.e., we are at a top of bottom border)
         continue
      
      for char_idx in range(start_idx-1, start_idx+num_of_digits+1):  # look at every character between the column before and column after number
         if char_idx < 0 or char_idx > len(row)-1 or row[char_idx].isdigit(): # skip over digits and indices that are out-of-bounds
            continue
         adjacency_list.append( row[char_idx] )

   return adjacency_list

def get_gears( line_list: list, star_idx: int ) -> list:
   gears = []  # will be list of integers if applicable
   # iterate row-by-row
   for row in line_list:
      if not row: # if row is empty (i.e., we are at a top of bottom border)
         continue
      
      for char_idx in range(star_idx-1, star_idx+num_of_digits+1):  # look at every character between the column before and column after number
         if char_idx < 0 or char_idx > len(row)-1 or row[char_idx].isdigit(): # skip over digits and indices that are out-of-bounds
            continue
         adjacency_list.append( row[char_idx] )

   return adjacency_list
      

#################### ----MAIN----- #################### 

with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

# TODO:  Since the idea of adjacency is involved here, I really think a graph where each node is one of the characters
#        in the file, linked to its adjacent nodes, would be an idea here. Would like to explore that.

# I am going to treat the puzzle input text file as a 2d grid which it just so happens to be.
# This'll help me define adjacency.
part_numbers = [] # will become a list of numbers
for line_idx,line in enumerate(puzzle_input_lines):

   line = line.strip()
   loop_skip_counter = 0

   for char_idx,char in enumerate(line):

      # skip some characters if applicable
      if loop_skip_counter > 0:
         loop_skip_counter = loop_skip_counter - 1
         continue

      # find next number!
      (num_str, loop_skip_counter) = get_next_num_in_line_starting_at_idx( line, char_idx )
      if num_str == '':
         break # couldn't find a number so move on to next line!
      
      # get adjacency list
      # get list of lines before, current, and after, as applicable
      line_list = []
      for line_add_idx in range(line_idx-1, line_idx+2):
         if line_add_idx < 0 or line_add_idx > len(puzzle_input_lines)-1:
            line_list.append([])
         else:
            line_list.append(puzzle_input_lines[line_add_idx].strip())
      adjacency_list = get_adjacency_list( line_list, char_idx+loop_skip_counter+1-len(num_str), len(num_str) )
      
      # check for special symbols and add part number if applicable
      # if the number of '.'s is less than the length of the adjacent chars list, then some of the chars must be other symbols
      # and we have ourselves a part number! we've also skipped over digits in making the adj list, so they shouldn't affect this.
      if adjacency_list.count('.') < len(adjacency_list):
         part_numbers.append(int(num_str))

total = 0
for num in part_numbers:
   total = total + num

print(f'Sum of part numbers:\t{total}')