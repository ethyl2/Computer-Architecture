"""
Given an object/dictionary with keys and values that consist of both strings and integers, 
design an algorithm to calculate and return the sum of all of the numeric values. 
For example, given the following object/dictionary as input:
```
{
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}
```
Your algorithm should return 41, the sum of the values 23 and 18. 
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. 
Run through the UPER problem solving framework while going through your thought process. 
"""
# Total variable set
total = 0
my_dict = {
    "cat": "bob",
    "dog": 23,
    19: 18,
    90: "fish"
}

# Convert dict to list of values

# Loop through values
# If type of value == int: add to total
for value in my_dict.values():
    if type(value) == int:
        total += value
# Return the total
print(total)
