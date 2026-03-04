# 1. Create a variable named pi and store the value 22/7 in it.
# Now check the data type of this variable.

pi = 22/7
print("Value of pi:", pi)
print("Data type of pi:", type(pi))


# 2. Create a variable called for and assign it a value 4.
# See what happens and find the reason.

# for = 4   # Uncommenting this line will cause an error

print("\nQuestion 2:")
print("We cannot use 'for' as a variable name.")
print("Reason: 'for' is a reserved keyword in Python used in loops.")


# 3. Store principal, rate, and time in variables and calculate Simple Interest
# Formula: SI = (P * R * T) / 100

principal = 10000   # Principal amount
rate = 8            # Rate of interest (%)
time = 3            # Time in years

simple_interest = (principal * rate * time) / 100

print("\nQuestion 3:")
print("Principal:", principal)
print("Rate:", rate)
print("Time:", time)
print("Simple Interest:", simple_interest)
