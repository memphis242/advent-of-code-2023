PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day1/python/puzzle-input.txt'

# REMEMBER TO TO-LOWERCASE!
DIGITS_SPELLED_OUT = \
[                    \
   'zero',           \
   'one',            \
   'two',            \
   'three',          \
   'four',           \
   'five',           \
   'six',            \
   'seven',          \
   'eight',          \
   'nine'            \
]

DIGIT_DICTIONARY =   \
{
   'z': ['zero'],
   'o': ['one'],
   't': ['two', 'three'],
   'f': ['four', 'five'],
   's': ['six', 'seven'],
   'e': ['eight'],
   'n': ['nine']
}

SPELLED_DIGIT_TO_NUM_MAP = \
{
   'zero':  '0',
   'one':   '1',
   'two':   '2',
   'three': '3',
   'four':  '4',
   'five':  '5',
   'six':   '6',
   'seven': '7',
   'eight': '8',
   'nine':  '9'
}

with open(PUZZLE_INPUT, 'r') as puzzle_input_file:
   puzzle_input_lines = puzzle_input_file.readlines()

# print(puzzle_input_lines[0])
# print(puzzle_input_lines[1])
# print(puzzle_input_lines[2])

calibration_values = []
for line in puzzle_input_lines:

   line = line.strip()  # remove non-characters
   
   # Reset digits read in every loop!
   first_digit = ''
   last_digit = ''
   last_digit_read = ''

   for idx, character in enumerate(line):
      
      # check for direct digit match
      if character.isdigit() == True:
         last_digit_read = character
         if first_digit == '':   # i.e., first digit still not found
            first_digit = character

      # check for spelled-out digit
      else:
         spelled_out_digit = ''
         digit_list = DIGIT_DICTIONARY.get(character, [])
         if digit_list:  # if key mapped to an existing item in the dictionary
            num_of_chars_left_in_line = len(line) - (idx + 1)  # make sure there are enough chars remaining!
            for spelled_digit in digit_list:
               # string formed by current char plus (len(spelled_digit)-1) chars to the right...
               if (len(spelled_digit) - 1) > num_of_chars_left_in_line:
                  continue

               spelled_digit_len = len(spelled_digit)
               # check_string = line[ idx : (len(spelled_digit)+1) ]
               if idx == 0:
                  check_string = line[ idx : spelled_digit_len ]
               elif num_of_chars_left_in_line == (spelled_digit_len-1):
                  check_string = line[ idx : -1 ] + line[-1]
               else:
                  check_string = line[ idx : (idx+spelled_digit_len) ]
               if check_string == spelled_digit:
                  last_digit_read = SPELLED_DIGIT_TO_NUM_MAP.get(spelled_digit, last_digit_read)
                  if first_digit == '':   # i.e., first digit still not found
                     first_digit = last_digit_read
                  break
            # TODO: Skip number of characters if match was found!

   last_digit = last_digit_read
   calibration_values.append( int(first_digit + last_digit) )

# print(calibration_values[0])
# print(calibration_values[1])
# print(calibration_values[2])

total = 0
for num in calibration_values:
   total = total + num

print(total)