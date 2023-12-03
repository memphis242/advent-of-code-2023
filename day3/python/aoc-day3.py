# TODO: Update to be relative path and configure debugger's working directory to here so you can debug with file inputs...
PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day3/python/day3-puzzle-input.txt'

#################### --CONSTANTS-- #################### 


#################### --FUNCTIONS-- #################### 
def get_next_num_in_line(line: str) -> int:
   return 0

#################### ----MAIN----- #################### 

with open(PUZZLE_INPUT, 'r') as puzzle_input:
   puzzle_input_lines = puzzle_input.readlines()

# TODO:  Since the idea of adjacency is involved here, I really think a graph where each node is one of the characters
#        in the file, linked to its adjacent nodes, would be an idea here. Would like to explore that.

# I am going to treat the puzzle input text file as a 2d grid which it just so happens to be.
# This'll help me define adjacency.
part_numbers = [] # will become a list of numbers
loop_skip_counter = 0
for line_idx,line in enumerate(puzzle_input_lines):
   for char_idx,char in enumerate(line):
      # find next number!

      # skip some characters if applicable
      if loop_skip_counter > 0:
         loop_skip_counter = loop_skip_counter - 1
         continue

      # if we are at a number, then get the number and find what color it was for
      if char.isdigit():
         # get the number
         num = 0
         num_str = char
         check_idx = char_idx+1
         check_char = line[check_idx]  # TODO: Careful of out-of-bounds reach
         while check_char.isdigit():
            num_str = num_str + check_char
            check_idx = check_idx + 1
            check_char = line[check_idx] # TODO: Careful of out-of-bounds reach
         num = int(num_str)
         loop_skip_counter = len(num_str) - 1  # rest of digits of number

         # Build adjacency list.
         # The first digit of a number should have the 3 spots to its left and the spots above and below it checked.
         # The middle digits of a number should just have their top and bottom spots checked.
         # The last digit of a number should have the 3 spots to its _right_ and the spots above and below it checked.
         # So for all digits, check above and below. For first digit, also left 3, and for last digit, also right 3.
         adjacent_chars = []
         at_top_row = False
         at_bottom_row = False
         at_left_col = False
         at_right_col = False
         for digit_idx,digit in enumerate(num_str):
            
            # check if we are at an edge
            if line_idx == 0:
               at_top_row = True
            elif char_idx == 0:
               at_left_col = True
            elif line_idx == ( len(puzzle_input_lines)-1 ):
               at_bottom_row = True
            elif char_idx == ( len(line)-1 ):
               at_right_col = True

            # Set a reference cell to start from. This'll be top left of the current **char** adjacency (**not** digit adjacency)
            # TODO: Maybe just use digit adjacency?
            # NOTE! First digit and current char are the same.
            STARTING_COL = char_idx - 1
            STARTING_ROW = line_idx - 1

            # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
            # NOTE: Only append non-digits to the list; makes the following checks easier
            # NOTE: The way the input is structured, you **can't** be _both_ at the left _and_ the right, or at the top _and_ the bottom.
            #       I'll take advantage of that by not checking certain paths.
            if at_top_row == True:

               # if we are at the top-left or top-right most part of the file or mid-number
               if at_left_col == True or at_right_col == True or ( at_left_col == False and at_right_col == False and digit_idx != (len(num_str)-1) and digit_idx != 0 ): 
                  # check just bottom
                  char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                  # only append non-digits to the list; makes the following checks easier
                  # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
                  if not char_bottom.isdigit():
                     adjacent_chars.append(char_bottom)

               elif digit_idx == 0: # first digit
                  # check lefts and bottom
                  char_left         = puzzle_input_lines[STARTING_ROW+1][STARTING_COL  ]
                  char_bottom_left  = puzzle_input_lines[STARTING_ROW+2][STARTING_COL  ]
                  char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+1]
                  # only append non-digits to the list; makes the following checks easier
                  if not char_left.isdigit():
                     adjacent_chars.append(char_left)
                  if not char_bottom_left.isdigit():
                     adjacent_chars.append(char_bottom_left)
                  if not char_bottom.isdigit():
                     adjacent_chars.append(char_bottom)

               else: # we are at the top border, somewhere in the middle
                  # get bottom and rights
                  char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                  char_right        = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx+2]
                  char_bottom_right = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+2]
                  if not char_bottom.isdigit():
                     adjacent_chars.append(char_bottom)
                  if not char_right.isdigit():
                     adjacent_chars.append(char_right)
                  if not char_bottom_right.isdigit():
                     adjacent_chars.append(char_bottom_right)

            elif at_bottom_row == True:

               # if we are at the bottom-left or bottom-right most part of the file or mid-number
               if at_left_col == True or at_right_col == True or ( at_left_col == False and at_right_col == False and digit_idx != (len(num_str)-1) ): 
                  # check just top
                  char_top       = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+1]
                  # only append non-digits to the list; makes the following checks easier
                  # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
                  if not char_top.isdigit():
                     adjacent_chars.append(char_top)

               else: # we are at the bottom border, somewhere in the middle
                  # get top and rights
                  char_top       = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+1]
                  char_right     = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx+2]
                  char_top_right = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+2]
                  if not char_top.isdigit():
                     adjacent_chars.append(char_top)
                  if not char_right.isdigit():
                     adjacent_chars.append(char_right)
                  if not char_top_right.isdigit():
                     adjacent_chars.append(char_top_right)

            else: # we are not along the border

               if digit_idx == 0:   # if we are at the first digit
                  # check lefts and top and bottom
                  char_top_left     = puzzle_input_lines[STARTING_ROW  ][STARTING_COL  ]
                  char_left         = puzzle_input_lines[STARTING_ROW+1][STARTING_COL  ]
                  char_bottom_left  = puzzle_input_lines[STARTING_ROW+2][STARTING_COL  ]
                  char_top          = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+1]
                  char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+1]
                  # only append non-digits to the list; makes the following checks easier
                  if not char_top_left.isdigit():
                     adjacent_chars.append(char_top_left)
                  if not char_left.isdigit():
                     adjacent_chars.append(char_left)
                  if not char_bottom_left.isdigit():
                     adjacent_chars.append(char_bottom_left)
                  if not char_top.isdigit():
                     adjacent_chars.append(char_top)
                  if not char_bottom.isdigit():
                     adjacent_chars.append(char_bottom)

               elif digit_idx == len(num_str)-1:   # if we are at the last digit
                  # check right 3 and top and top
                  char_top           = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+1]
                  char_bottom        = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                  char_top_right     = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+2]
                  char_right         = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx+2]
                  char_bottom_right  = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+2]
                  if not char_top_right.isdigit():
                     adjacent_chars.append(char_top_right)
                  if not char_right.isdigit():
                     adjacent_chars.append(char_right)
                  if not char_top_right.isdigit():
                     adjacent_chars.append(char_top_right)
                  if not char_top.isdigit():
                     adjacent_chars.append(char_top)
                  if not char_bottom.isdigit():
                     adjacent_chars.append(char_bottom)

               else:   # we are at a middle digit
                  # check just top and bottom
                  char_top           = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+1]
                  char_bottom        = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                  if not char_top.isdigit():
                     adjacent_chars.append(char_top)
                  if not char_bottom.isdigit():
                     adjacent_chars.append(char_bottom)

         # if the number of '.'s is less than the length of the adjacent chars list, then some of the chars must be other symbols
         # and we have ourselves a part number!
         if adjacent_chars.count('.') < len(adjacent_chars):
            part_numbers.append(num)


total = 0
for num in part_numbers:
   total = total + num

print(f'Sum of part numbers:\t{total}')