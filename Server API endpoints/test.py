my_dict = {"1": "a", "3": "c", "2": "b"}

# Convert dictionary values to a list and sort by keys
sorted_values = [value for key, value in sorted(my_dict.items())]

print(sorted_values)