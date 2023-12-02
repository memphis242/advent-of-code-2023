PUZZLE_INPUT = 'C:/git/aoc/advent-of-code-2023/day1/python/puzzle-input.txt'

with open(PUZZLE_INPUT, 'r') as puzzle_input_file:
   puzzle_input_lines = puzzle_input_file.readlines()

# print(puzzle_input_lines[0])
# print(puzzle_input_lines[1])
# print(puzzle_input_lines[2])

calibration_values = []
for line in puzzle_input_lines:
   
   # Reset digits read in every loop!
   first_digit = ''
   last_digit = ''
   last_digit_read = ''

   for character in line:
      if character.isdigit() == True:
         last_digit_read = character
         if first_digit == '':   # i.e., first digit still not found
            first_digit = character
   last_digit = last_digit_read
   calibration_values.append( int(first_digit + last_digit) )

# print(calibration_values[0])
# print(calibration_values[1])
# print(calibration_values[2])

total = 0
for num in calibration_values:
   total = total + num

print(total)