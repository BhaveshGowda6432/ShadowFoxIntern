# Initial Justice League members
justice_league = ["Superman", "Batman", "Wonder Woman", "Flash", "Aquaman", "Green Lantern"]

print("Initial List:", justice_league)


# 1. Calculate the number of members
print("\n1. Number of members:", len(justice_league))


# 2. Add Batgirl and Nightwing to the list
justice_league.append("Batgirl")
justice_league.append("Nightwing")
print("\n2. After adding Batgirl and Nightwing:", justice_league)


# 3. Move Wonder Woman to the beginning (leader)
justice_league.remove("Wonder Woman")   # Remove from current position
justice_league.insert(0, "Wonder Woman")  # Insert at index 0
print("\n3. After making Wonder Woman leader:", justice_league)


# 4. Separate Aquaman and Flash
# We will move "Superman" between Aquaman and Flash
justice_league.remove("Superman")

# Find position of Aquaman
aquaman_index = justice_league.index("Aquaman")

# Insert Superman after Aquaman
justice_league.insert(aquaman_index + 1, "Superman")
print("\n4. After separating Aquaman and Flash:", justice_league)


# 5. Replace entire team with new members
justice_league = ["Cyborg", "Shazam", "Hawkgirl", "Martian Manhunter", "Green Arrow"]
print("\n5. New Justice League team:", justice_league)


# 6. Sort alphabetically
justice_league.sort()
print("\n6. Sorted Justice League:", justice_league)

# New leader is the hero at index 0
print("New Leader:", justice_league[0])
