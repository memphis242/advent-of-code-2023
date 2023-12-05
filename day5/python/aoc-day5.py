#################### ---IMPORTS--- #################### 
from typing import Tuple, List

#################### --CONSTANTS-- #################### 
# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day5/python/day5-puzzle-input.txt'
TEST_INPUT = 'C:/git/aoc/advent-of-code-2023/day5/python/day5-test-input.txt'

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
# TODO: create a ~~dictionary for each mapping~~ list of graphs that lays out the map from seed to location.

with open(TEST_INPUT, 'r') as puzzle_input:
# with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

# get list of initial seeds
INITIAL_SEEDS_LINE_IDX = 0
initial_seeds_line = puzzle_input_lines[INITIAL_SEEDS_LINE_IDX]
initial_seeds = []
loop_skip_counter = 0
for char_idx, char in enumerate(initial_seeds_line):
   # skip characters if applicable
   if loop_skip_counter > 0:
      loop_skip_counter -= 1
      continue
   ( seed_num, loop_skip_counter ) = get_next_num_in_line_starting_at_idx( initial_seeds_line, char_idx )
   if seed_num == '':
      continue
   initial_seeds.append(seed_num)

print(initial_seeds)

# gonna try to be efficient and traverse directly through the seed-to-location mapping
# first create tuples that specify ranges to check against to determine if the mapping is simple or specific


for seed in initial_seeds:
   # figure out what fertilizer this seed maps to
   # see if this seed is within range of specific mapping or the soil number will just be the same
   


# # this is probably inefficient because i only really care about the mapping between seed and location...
# # also, i don't know how python implements the hashing function needed for dictionary mapping and how efficient that is...
# seed_to_soil_map = dict.fromkeys(range(0,+1), 0)
# soil_to_fertilizer_map = {}
# fertilizer_to_water_map = {}
# for line_idx,line in enumerate(puzzle_input_lines):
# 
#    line = line.strip()
#    loop_skip_counter = 0
# 
#    # develop mappings indicated by line
#    for char_idx,char in enumerate(card):
# 
#       # skip some characters if applicable
#       if loop_skip_counter > 0:
#          loop_skip_counter = loop_skip_counter - 1
#          continue
# 
#       # skip over non-digits except for the vertical bar
#       if not char.isdigit() and char != '|':
#          continue
# 
#       # find next number!
#       (num_str, loop_skip_counter) = get_next_num_in_line_starting_at_idx( card, char_idx )
#       if num_str == '':
#          break # couldn't find a number so move on to next card!
#       active_list.append(int(num_str))
# 
#    # create location list from mappings
# 
# 
#    # find min location
# 
# 
# # sum up points!
# total_points = 0
# for num in card_values:
#    total_points = total_points + num
# 
# print(f'Part 1: {total_points} card points')
# print(f'Part 2: {num_of_card_copies} number of card copies')
# 