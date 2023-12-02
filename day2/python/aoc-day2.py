# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day2/python/day2-puzzle-input.txt'

#################### --CONSTANTS-- #################### 
# from the problem statement
PROBLEM_STATEMENT_MAXES = { 'red': 12, 'green': 13, 'blue': 14 }
# some useful observatiosn
GAME_ID_START_IDX = 5


#################### --FUNCTIONS-- #################### 
# TODO: Make game_id an optional argument
def color_maxes_in_line( line: str, game_id: str ) -> dict:
   ret_max_of_each_color = {'red': 0, 'green': 0, 'blue': 0}
   # slice string to skip over "Game xyz: " part
   sliced_line = line[ (GAME_ID_START_IDX+len(game_id)-1) : ]
   current_color = ''
   loop_skip_counter = 0
   for idx,char in enumerate(sliced_line):
      # skip some characters if applicable
      if loop_skip_counter > 0:
         loop_skip_counter = loop_skip_counter - 1
         continue

      # if we are at a number, then get the number and find what color it was for
      if char.isdigit():
         # get the number
         num = 0
         num_str = char
         check_idx = idx+1
         check_char = sliced_line[check_idx]  # TODO: Careful of out-of-bounds reach
         while check_char.isdigit():
            num_str = num_str + check_char
            check_idx = check_idx + 1
            check_char = sliced_line[check_idx] # TODO: Careful of out-of-bounds reach
         check_idx = check_idx + 1  # skip space after digits
         num = int(num_str)
         loop_skip_counter = len(num_str) + 1   # digits of number + space afterwards

         # find what color it is for
         check_char = sliced_line[check_idx]
         current_color = ''
         match check_char:
            case 'r':
               current_color = 'red'
               loop_skip_counter = loop_skip_counter + 3    # skip over letters
            
            case 'g':
               current_color = 'green'
               loop_skip_counter = loop_skip_counter + 5    # skip over letters

            case 'b':
               current_color = 'blue'
               loop_skip_counter = loop_skip_counter + 4    # skip over letters

         # compare against max of line for that color thus far and update if applicable
         if current_color != '' and num > ret_max_of_each_color[current_color]:
               ret_max_of_each_color[current_color] = num

   return ret_max_of_each_color

def get_game_line_id( line: str ) -> int:
   ret_str = ''
   # we'll take advantage of the pattern that every line starts with "Game x", so the number always starts at index 5 (0-indexed) of the line.
   # get the first digit that'll always exist
   ret_str = line[GAME_ID_START_IDX]
   # slice the "Game x" part of the line
   sliced_line = line[GAME_ID_START_IDX+1:]
   for char in sliced_line:
      if char.isdigit():
         ret_str = ret_str + char
      else:
         break
   
   return int(ret_str)


#################### ----MAIN----- #################### 
puzzle_input_lines = []
with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

# QUICK-CHECK
# print( get_game_line_id( puzzle_input_lines[85] ) )
# print( color_maxes_in_line( puzzle_input_lines[87], '1' ) )

# get game id's and color maxes for each game
game_ids = []  # will be list of numbers representing game id's
game_color_maxes = []   # will be a list of dictionaries of the max of each color for each game
for line in puzzle_input_lines:
   # get game id
   game_id = get_game_line_id(line)
   game_ids.append(game_id)
   # find the max of each color in each line
   game_color_maxes.append( color_maxes_in_line( line, str(game_id) ) )

possible_games = []  # will be list of numbers representing possible game id's
for game_id, game_max_dict in zip(game_ids, game_color_maxes):
   if game_max_dict['red']    <= PROBLEM_STATEMENT_MAXES['red']   and \
      game_max_dict['blue']   <= PROBLEM_STATEMENT_MAXES['blue']  and \
      game_max_dict['green']  <= PROBLEM_STATEMENT_MAXES['green']:

      possible_games.append(game_id)

# sum over games!
total = 0
for game_id in possible_games:
   total = total + game_id

print(total)