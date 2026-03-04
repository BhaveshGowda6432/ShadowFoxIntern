# -----------------------------------
# 1. BMI Category Program
# -----------------------------------

# Take user input
height = float(input("Enter height in meters: "))
weight = float(input("Enter weight in kilograms: "))

# BMI formula: weight / height^2
bmi = weight / (height ** 2)

# Determine BMI category using if-elif
if bmi >= 30:
    print("Obesity")
elif bmi >= 25:
    print("Overweight")
elif bmi >= 18.5:
    print("Normal")
else:
    print("Underweight")


# -----------------------------------
# 2. City → Country Finder
# -----------------------------------

# Lists of cities
australia = ["Sydney", "Melbourne", "Brisbane", "Perth"]
uae = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"]
india = ["Mumbai", "Bangalore", "Chennai", "Delhi"]

city = input("\nEnter a city name: ")

# Check which country the city belongs to
if city in australia:
    print(city, "is in Australia")
elif city in uae:
    print(city, "is in UAE")
elif city in india:
    print(city, "is in India")
else:
    print("City not found in database")


# -----------------------------------
# 3. Check if Two Cities Belong to Same Country
# -----------------------------------

city1 = input("\nEnter the first city: ")
city2 = input("Enter the second city: ")

# Function to find country of a city
def find_country(city):
    if city in australia:
        return "Australia"
    elif city in uae:
        return "UAE"
    elif city in india:
        return "India"
    else:
        return None

# Get countries
country1 = find_country(city1)
country2 = find_country(city2)

# Compare countries
if country1 and country1 == country2:
    print(f"Both cities are in {country1}")
else:
    print("They don't belong to the same country")
