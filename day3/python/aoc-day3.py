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

            # set a reference cell to start from; NOTE! assuming we aren't at the border
            STARTING_COL = char_idx - 1
            STARTING_ROW = line_idx - 1

            if at_top_row == True:
               if at_left_col == True:
                  # we are at the top-left most part of the file

                  if digit_idx == len(num_str)-1:   # if we are at the last digit
                     # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
                     # only append non-digits to the list; makes the following checks easier
                     char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                     if not char_bottom.isdigit():
                        adjacent_chars.append(char_bottom)
                     
                     # make sure there's another column to the right!
                     num_of_chars_remaining_in_line = len(line) - (char_idx + len(num_str))
                     if num_of_chars_remaining_in_line > 0:
                        char_right        = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx+2]
                        char_bottom_right = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+2]
                        if not char_right.isdigit():
                           adjacent_chars.append(char_right)
                        if not char_bottom_right.isdigit():
                           adjacent_chars.append(char_bottom_right)

                  else:   # we are at first or middle digits
                     # check just bottoms
                     char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                     # only append non-digits to the list; makes the following checks easier
                     # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
                     if not char_bottom.isdigit():
                        adjacent_chars.append(char_bottom)

               elif at_right_col == True:
                  #

               else:
                  # we are at the top border, somewhere in the middle

                  if digit_idx == len(num_str)-1:   # if we are at the last digit
                     # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
                     # only append non-digits to the list; makes the following checks easier
                     char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                     if not char_bottom.isdigit():
                        adjacent_chars.append(char_bottom)
                     
                     # make sure there's another column to the right!
                     num_of_chars_remaining_in_line = len(line) - (char_idx + len(num_str))
                     if num_of_chars_remaining_in_line > 0:
                        char_right        = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx+2]
                        char_bottom_right = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+2]
                        if not char_right.isdigit():
                           adjacent_chars.append(char_right)
                        if not char_bottom_right.isdigit():
                           adjacent_chars.append(char_bottom_right)

                  elif digit_idx == 0: # we are at the first digit
                     # check left and bottom
                     char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                     if not char_bottom.isdigit():
                        adjacent_chars.append(char_bottom)
                     char_left         = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx  ]
                     if not char_left.isdigit():
                        adjacent_chars.append(char_left)
                     char_bottom_left  = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx  ]
                     if not char_bottom_left.isdigit():
                        adjacent_chars.append(char_bottom_left)

                  else:   # we are at middle digits
                     # check just bottoms
                     char_bottom       = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                     # only append non-digits to the list; makes the following checks easier
                     # TODO: Learn about passing around mutable lists/strings by reference in Python so you can function-this-out!!
                     if not char_bottom.isdigit():
                        adjacent_chars.append(char_bottom)

            elif at_bottom_row == True:
               if at_left_col == True:
                  #

               elif at_right_col == True:
                  # 

               
               else:
                  #


            else: # we are not along the border
               if digit_idx == 0:   # if we are at the first digit
                  # check left 3 and top and bottom
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
                  # check right 3 and top and bottom
                  char_top           = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+1]
                  char_bottom        = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                  char_top_right     = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+2]
                  char_right         = puzzle_input_lines[STARTING_ROW+1][STARTING_COL+digit_idx+2]
                  char_bottom_right  = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+2]
                  adjacent_chars.append(char_top_right)
                  adjacent_chars.append(char_right)
                  adjacent_chars.append(char_bottom_right)
                  adjacent_chars.append(char_top)
                  adjacent_chars.append(char_bottom)

               else:   # we are at a middle digit
                  # check just top and bottom
                  char_top           = puzzle_input_lines[STARTING_ROW  ][STARTING_COL+digit_idx+1]
                  char_bottom        = puzzle_input_lines[STARTING_ROW+2][STARTING_COL+digit_idx+1]
                  adjacent_chars.append(char_top)
                  adjacent_chars.append(char_bottom)

         # if the number of '.'s is less than the length of the adjacent chars list, then some of the chars must be other symbols
         # and we have ourselves a part number!
         if adjacent_chars.count('.') < len(adjacent_chars):
            part_numbers.append(num)


total = 0
for num in part_numbers:
   total = total + num

print(f'Sum of part numbers:\t{total}')