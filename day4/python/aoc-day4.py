#################### ---IMPORTS--- #################### 
from typing import Tuple, List


# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day4/python/day4-puzzle-input.txt'

#################### --CONSTANTS-- #################### 
WINNING_NUMBERS_START_COL = 10

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

card_values = [] # will become a list of numbers
original_num_of_cards = len(puzzle_input_lines)
card_copies = dict.fromkeys(range(1,original_num_of_cards+1), 1)
for card_idx,card in enumerate(puzzle_input_lines):

   card = card.strip()
   loop_skip_counter = 0

   # get winning numbers list and your numbers list
   winning_numbers = []
   your_numbers = []
   active_list = winning_numbers
   found_start = False
   for char_idx,char in enumerate(card):
      if found_start == False and char != ':':
         continue
      elif char == ':':
         found_start = True
         continue # skip over this colon character

      # skip some characters if applicable
      if loop_skip_counter > 0:
         loop_skip_counter = loop_skip_counter - 1
         continue

      # skip over non-digits except for the vertical bar
      if not char.isdigit() and char != '|':
         continue

      if char == '|':
         active_list = your_numbers # switch reference over

      # find next number!
      (num_str, loop_skip_counter) = get_next_num_in_line_starting_at_idx( card, char_idx )
      if num_str == '':
         break # couldn't find a number so move on to next card!
      active_list.append(int(num_str))

   # compare the list of numbers and assign point to card
   card_points = 0
   num_of_matches = 0
   for num in your_numbers:
      if num in winning_numbers:
         num_of_matches = num_of_matches + 1
         if card_points == 0:
            card_points = 1
         else:
            card_points = card_points * 2
   card_values.append(card_points)
   for copy in range(0, card_copies[card_idx + 1]):
      for i in range(1,num_of_matches+1):
         if (card_idx+i+1) > original_num_of_cards:
            break    # can't go past end of table
         card_copies[card_idx+i+1] = card_copies[card_idx+i+1] + 1

# sum up points!
total_points = 0
for num in card_values:
   total_points = total_points + num

# sum of card copies
num_of_card_copies = 0
for key in card_copies.keys():
   num_of_card_copies = num_of_card_copies + card_copies[key]

print(f'Part 1: {total_points} card points')
print(f'Part 2: {num_of_card_copies} number of card copies')