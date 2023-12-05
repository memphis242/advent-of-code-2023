#################### ---IMPORTS--- #################### 
from typing import Tuple, List
import sys
import time

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
# TODO: create a ~~dictionary for each mapping~~ list of graphs that lays out the map from seed to location.
# strategy: traverse directly from seed to location without creating every mapping first

# with open(TEST_INPUT, 'r') as puzzle_input:
with open(PUZZLE_INPUT, 'r') as puzzle_input:
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

# part 2: create list of doubles representing seed ranges to check
seed_ranges = []  # list of doubles
skip_next = False
for i in range(0,len(initial_seeds)):
   if skip_next:
      skip_next = False
      continue

   if i % 2 == 0:
      seed_ranges.append( (initial_seeds[i], initial_seeds[i+1]) )   # not going to bounds-check because we _should_ be guaranteed an even number of seeds
      skip_next = True

# for the terminal, i'd like to print out my progress in mapping each seed. to do that, i want to know how many seeds there are to process
num_of_seeds_to_process = 0
for double in seed_ranges:
   num_of_seeds_to_process += double[1]
print(f'{num_of_seeds_to_process:,}')

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
locations_part1 = []
for seed in initial_seeds:
   # map your way through!
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
   locations_part1.append( map_value( humidity_val,   mappings[HUMIDITY_TO_LOCATION_IDX]  ) )

# i shouldn't build a list for part 2 since the ranges are absolutely massive
# to at least save on memory complexity, i'll keep track of the min as i go along
min_location = None
min_location_seed = None
num_of_seeds_processed = 0
start_time = time.time()
for seed_range in seed_ranges:
   # gotta iterate through every possible seed number in every range!
   for seed in range( seed_range[0], seed_range[0]+seed_range[1] ):
      # map your way through!
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
      location_val  = map_value( humidity_val,    mappings[HUMIDITY_TO_LOCATION_IDX]  )
      if min_location == None:
         min_location = location_val
         min_location_seed = seed
      elif min_location > location_val:
         min_location = location_val
         min_location_seed = seed
      
      num_of_seeds_processed += 1
      updated_time = time.time() - start_time
      printProgressBar( num_of_seeds_processed, num_of_seeds_to_process, prefix=f'{num_of_seeds_processed:,} seeds processed out of {num_of_seeds_to_process:,}', suffix=f'time passed: {updated_time}' )

# find min of locations list; its index will be the same as the index of the seed that mapped to it
minimum_location_part1 = min(locations_part1)
minimum_location_part1_idx = locations_part1.index(minimum_location_part1) # NOTE! min may not be unique; this just returns first occurence i think
seed_that_mapped_to_min_part1 = initial_seeds[minimum_location_part1_idx]

print(f'Part 1:\tMin Location: {minimum_location_part1}, (Possible) Corresponding Seed: {seed_that_mapped_to_min_part1}')
print(f'Part 2:\tMin Location: {min_location}, (Possible) Corresponding Seed: {min_location_seed}')