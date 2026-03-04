# 1. Function using format()

# This function takes a number and a format type
# and returns the formatted string using Python's format() function
def format_number(num, fmt):
    return format(num, fmt)

# Call the function with 145 and 'o'
# 'o' converts decimal number into octal (base-8)
result = format_number(145, 'o')

print("Formatted result:", result)
# 145 in decimal = 221 in octal
print("Representation used: Octal (base 8)")


# 2. Circular pond problem

# Given values
pi = 3.14
radius = 84  # meters

# Area of circle formula: πr²
# area = 3.14 × 84 × 84
area = pi * radius * radius

# Water per square meter
water_per_sqm = 1.4

# Total water = area × water per square meter
total_water = area * water_per_sqm

# int() removes decimal part as required in the question
print("\nArea of pond:", area, "square meters")
print("Total water in pond:", int(total_water), "liters")


# 3. Speed calculation

# Given distance in meters
distance = 490

# Time is given in minutes, convert to seconds
time_minutes = 7
time_seconds = time_minutes * 60  # 1 minute = 60 seconds

# Speed formula: Speed = Distance / Time
speed = distance / time_seconds

# Remove decimals using int()
print("\nSpeed:", int(speed), "meters per second")
