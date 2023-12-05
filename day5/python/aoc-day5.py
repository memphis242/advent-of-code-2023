#################### ---IMPORTS--- #################### 
from typing import Tuple, List

#################### --CONSTANTS-- #################### 
# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day5/python/day5-puzzle-input.txt'


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


#################### ----MAIN----- #################### 

with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

for line_idx,line in enumerate(puzzle_input_lines):

   line = line.strip()
   loop_skip_counter = 0

   # develop mappings indicated by line
   for char_idx,char in enumerate(card):

      # skip some characters if applicable
      if loop_skip_counter > 0:
         loop_skip_counter = loop_skip_counter - 1
         continue

      # skip over non-digits except for the vertical bar
      if not char.isdigit() and char != '|':
         continue

      # find next number!
      (num_str, loop_skip_counter) = get_next_num_in_line_starting_at_idx( card, char_idx )
      if num_str == '':
         break # couldn't find a number so move on to next card!
      active_list.append(int(num_str))

   # create location list from mappings


   # find min location


# sum up points!
total_points = 0
for num in card_values:
   total_points = total_points + num

print(f'Part 1: {total_points} card points')
print(f'Part 2: {num_of_card_copies} number of card copies')
