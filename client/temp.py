import ast

# Your input string
request = "ADD_TEST_RESULT [True, False, False, False] [True, True] http://testphp.vulnweb.com/artists.php?artist=1 user123@gmail.com"

# Split the input string by spaces
parts = request.split(' ')

# Extract the parts that make up the lists
list1_str_parts = parts[1:5]
list2_str_parts = parts[5:7]

# Join the parts to form complete list representations
joined_str1 = ' '.join(list1_str_parts)
joined_str2 = ' '.join(list2_str_parts)

# Convert the joined strings to actual lists using ast.literal_eval
list1 = ast.literal_eval(joined_str1)
list2 = ast.literal_eval(joined_str2)

# Print the lists to verify
print(list1)  # Output: [True, False, False, False]
print(list2)  # Output: [True, True]
