# Python Sets and Dictionaries

# Part 1 : Sets

---

# What is a Set?

A Set is a collection of unique elements.

Example:

```python
students = {"Hardik", "Rahul", "Amit"}
```

### Properties of Sets

* Unordered
* No duplicate values
* Mutable (can be changed)
* Uses curly braces {}

Example:

```python
numbers = {1,2,3,4}
```

---

# Why Do We Need Sets?

Suppose:

```python
names = ["Hardik","Rahul","Hardik","Amit","Rahul"]
```

Output contains duplicates.

Using Set:

```python
names = {"Hardik","Rahul","Amit"}
```

Duplicates are removed automatically.

---

# Creating Sets

### Method 1

```python
s = {1,2,3,4}
```

### Method 2

```python
s = set([1,2,3,4])
```

### Empty Set

Wrong:

```python
s = {}
```

This creates a dictionary.

Correct:

```python
s = set()
```

---

# Adding Elements

### add()

```python
s = {1,2,3}

s.add(4)

print(s)
```

Output:

```python
{1,2,3,4}
```

---

# Adding Multiple Elements

### update()

```python
s = {1,2,3}

s.update([4,5,6])

print(s)
```

---

# Removing Elements

### remove()

```python
s.remove(3)
```

### discard()

```python
s.discard(3)
```

Difference:

remove() gives error if element not found.

discard() does not.

---

# pop()

Removes a random element.

```python
s.pop()
```

---

# clear()

Removes everything.

```python
s.clear()
```

---

# Membership Operators

```python
"Python" in skills
```

```python
10 in numbers
```

Returns:

```python
True
False
```

---

# Set Operations

---

# Union

Combine all elements.

```python
a = {1,2,3}
b = {3,4,5}

print(a | b)
```

Output:

```python
{1,2,3,4,5}
```

---

# Intersection

Common elements.

```python
a & b
```

Output:

```python
{3}
```

---

# Difference

Elements present in first set only.

```python
a - b
```

Output:

```python
{1,2}
```

---

# Symmetric Difference

Elements not common.

```python
a ^ b
```

Output:

```python
{1,2,4,5}
```

---

# Converting List to Set

```python
numbers = [1,1,2,2,3,3]

unique = set(numbers)

print(unique)
```

Very important use case.

---

# Practice Questions

1. Create a set of 5 numbers.
2. Add an element.
3. Remove an element.
4. Find union.
5. Find intersection.
6. Remove duplicates from list.
7. Check membership.
8. Find difference.
9. Clear a set.
10. Count unique values in a list.

---

# Part 2 : Dictionaries

---

# What is a Dictionary?

Dictionary stores data in:

Key : Value format

Example:

```python
student = {
    "name":"Hardik",
    "age":22,
    "city":"Ahmedabad"
}
```

---

# Why Dictionaries?

Without Dictionary:

```python
name = "Hardik"
age = 22
city = "Ahmedabad"
```

With Dictionary:

```python
student = {
    "name":"Hardik",
    "age":22,
    "city":"Ahmedabad"
}
```

Everything is grouped together.

---

# Creating Dictionaries

```python
student = {
    "name":"Hardik",
    "age":22
}
```

---

# Accessing Values

```python
student["name"]
```

Output:

```python
Hardik
```

---

# Using get()

```python
student.get("name")
```

Safer method.

---

# Adding New Data

```python
student["city"] = "Ahmedabad"
```

---

# Updating Data

```python
student["age"] = 23
```

---

# Removing Data

### pop()

```python
student.pop("age")
```

---

### del

```python
del student["city"]
```

---

### clear()

```python
student.clear()
```

---

# Dictionary Methods

### keys()

```python
student.keys()
```

---

### values()

```python
student.values()
```

---

### items()

```python
student.items()
```

---

# Looping Through Dictionary

### Keys

```python
for key in student:
    print(key)
```

### Values

```python
for value in student.values():
    print(value)
```

### Key Value Pairs

```python
for key,value in student.items():
    print(key,value)
```

---

# Nested Dictionary

```python
students = {
    101:{
        "name":"Hardik",
        "age":22
    }
}
```

Access:

```python
students[101]["name"]
```

---

# Dictionary Comprehension

```python
squares = {x:x*x for x in range(5)}

print(squares)
```

---

# Frequency Counter

Very Important

```python
word = "banana"

freq = {}

for ch in word:
    freq[ch] = freq.get(ch,0)+1

print(freq)
```

Output:

```python
{
'b':1,
'a':3,
'n':2
}
```

---

# Real World Uses

Dictionary:

* Student Records
* Employee Data
* Product Data
* JSON Data
* API Responses

Set:

* Unique Values
* Duplicate Removal
* Membership Checking

---

# Practice Questions

1. Create a student dictionary.
2. Add city field.
3. Update age.
4. Delete a key.
5. Print all keys.
6. Print all values.
7. Loop through dictionary.
8. Count character frequency.
9. Create nested dictionary.
10. Create dictionary comprehension.

---

# Summary

Sets:

* Unique values
* No duplicates
* Union
* Intersection
* Difference

Dictionaries:

* Key value pairs
* Fast data access
* Most used data structure after Lists
* Widely used in APIs, ML and Data Analysis
