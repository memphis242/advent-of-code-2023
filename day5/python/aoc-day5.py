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

def map_value( val: int, triple_list: list ) -> int:
   DESTINATION_IDX = 0
   SOURCE_IDX = 1
   RANGE_IDX = 2

   # check if our val falls in the source range anywhere defined in the triple_list triples
   # recall the triple is ( destination_start, source_start, range )
   mapped_val = val  # assume mapped_val is the same as val. if val is within ranges defined in triple_list, for loop will change this value
   for triple in triple_list:
      if val >= triple[SOURCE_IDX] and val < (triple[SOURCE_IDX] + triple[RANGE_IDX]):
         # val is in range; map it
         mapped_val = triple[DESTINATION_IDX] + ( val - triple[SOURCE_IDX] )

   return mapped_val

#################### ----MAIN----- #################### 
# TODO: create a ~~dictionary for each mapping~~ list of graphs that lays out the map from seed to location.

with open(TEST_INPUT, 'r') as puzzle_input:
# with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

# get list of initial seeds
INITIAL_SEEDS_LINE_IDX = 0
initial_seeds_line = puzzle_input_lines[INITIAL_SEEDS_LINE_IDX].strip()
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
   initial_seeds.append(int(seed_num))

print(initial_seeds)

# strategy: traverse directly through the seed-to-location mapping instead of creating all the mappings first

# first parse through file and create lists of triples that specify ranges
MAPPINGS_START_LINE_IDX = 2
mappings =                          \
[                                   \
   # TODO: define enum!
   [], # 0 seeds_and_soils
   [], # 1 soils_and_fertilizers
   [], # 2 fertilizers_and_waters
   [], # 3 waters_and_lights
   [], # 4 lights_and_temps
   [], # 5 temps_and_humidities
   [], # 6 humidities_and_locations
]
active_idx = -1 # start /w seeds_and_soils
for line_idx, line in enumerate(puzzle_input_lines[MAPPINGS_START_LINE_IDX:]):
   line = line.strip()

   # skip over blank lines
   if not line:
      continue

   # move to next list mapping if applicable and skip line
   if ':' in line:
      active_idx += 1
      continue

   # get our triple!
   mappings[active_idx].append( get_mapping_triple( line ) )

# build list of locations
locations = []
for seed in initial_seeds:
   # figure out what fertilizer this seed maps to
   # see if this seed is within range of specific mapping or the soil number will just be the same
   SEED_TO_SOIL_IDX           = 0
   SOIL_TO_FERTILIZER_IDX     = 1
   FERTILIZER_TO_WATER_IDX    = 2
   WATER_TO_LIGHT_IDX         = 3
   LIGHT_TO_TEMP_IDX          = 4
   TEMP_TO_HUMIDITY_IDX       = 5
   HUMIDITY_TO_LOCATION_IDX   = 6
   soil_val       = map_value( seed,            mappings[SEED_TO_SOIL_IDX]          )
   fertilizer_val = map_value( soil_val,        mappings[SOIL_TO_FERTILIZER_IDX]    )
   water_val      = map_value( fertilizer_val,  mappings[FERTILIZER_TO_WATER_IDX]   )
   light_val      = map_value( water_val,       mappings[WATER_TO_LIGHT_IDX]        )
   temp_val       = map_value( light_val,       mappings[LIGHT_TO_TEMP_IDX]         )
   humidity_val   = map_value( temp_val,        mappings[TEMP_TO_HUMIDITY_IDX]      )
   locations.append( map_value( humidity_val,   mappings[HUMIDITY_TO_LOCATION_IDX]  ) )

# find min of locations list; its index will be the same as the index of the seed that mapped to it
minimum_location = min(locations)
minimum_location_idx = locations.index(minimum_location) # NOTE! min may not be unique; this just returns first occurence i think
seed_that_mapped_to_min = initial_seeds[minimum_location_idx]

print(f'Part 1:\t\tMin Location: {minimum_location}, (Possible) Corresponding Seed: {seed_that_mapped_to_min}')

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