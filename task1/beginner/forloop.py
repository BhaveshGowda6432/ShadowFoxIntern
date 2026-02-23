import random  # Used to generate random dice values

rolls = 20  # Number of dice rolls (at least 20)
count_6 = 0
count_1 = 0
two_sixes_in_row = 0

previous_roll = None

for i in range(rolls):
    roll = random.randint(1, 6)  # Simulate dice (1–6)
    print("Roll", i + 1, "=", roll)

    # Count number of 6s
    if roll == 6:
        count_6 += 1

    # Count number of 1s
    if roll == 1:
        count_1 += 1

    # Check two 6s in a row
    if previous_roll == 6 and roll == 6:
        two_sixes_in_row += 1

    previous_roll = roll  # Store last roll

# Print statistics
print("\nStatistics:")
print("Number of 6s:", count_6)
print("Number of 1s:", count_1)
print("Two 6s in a row:", two_sixes_in_row)

#---------------------------------------------------
#2. Jumping Jacks Workout Program
#---------------------------------------------------


total_jacks = 100
done = 0

# Loop in steps of 10 jumping jacks
for i in range(10, total_jacks + 1, 10):
    print("\nPerform 10 jumping jacks...")
    done += 10

    # Ask if tired
    tired = input("Are you tired? (yes/y or no/n): ").lower()

    if tired in ["yes", "y"]:
        skip = input("Do you want to skip the remaining workout? (yes/y or no/n): ").lower()

        if skip in ["yes", "y"]:
            print(f"You completed a total of {done} jumping jacks.")
            break
        else:
            remaining = total_jacks - done
            print(f"{remaining} jumping jacks remaining. Keep going!")

    # If finished all 100
    if done == total_jacks:
        print("Congratulations! You completed the workout.")
