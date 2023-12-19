import re

file_path = 'ls_cat.json'

with open(file_path, 'r') as file:
    data = file.read()

modified_data = re.sub(r'Cat.*:', lambda match: f'"{match.group()[:-1]}":', data)

with open(file_path, 'w') as file:
    file.write(modified_data)
