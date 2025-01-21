# Tentativa de corrigir strings com aspas abertas
with open('result1000p1000c.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Escrevendo um novo arquivo corrigido
with open('result1000p1000c_fixed.csv', 'w', encoding='utf-8') as file:
    for line in lines:
        # Remove quebras inesperadas de linha
        line = line.replace('\n', '').replace('\r', '')
        file.write(line + '\n')

# import json
# import random

# # Path to the uploaded file and the new output file
# input_file_path = 'utils/data/consumers1000.json'
# output_file_path = 'utils/data/consumers10000.json'

# # Load the existing consumers file
# with open(input_file_path, 'r', encoding='utf-8') as file:
#     consumers = json.load(file)

# # Generate 9000 new consumers with unique IDs and random attributes
# existing_count = len(consumers)
# new_consumers = []

# for i in range(existing_count + 1, existing_count + 9001):
#     new_consumer = {
#         "id": i,
#         "name": f"Consumer {i:04d}",
#         "budget": random.randint(80000, 120000),  # Random budget in range
#         "usage": random.randint(400, 1000)       # Random usage in range
#     }
#     new_consumers.append(new_consumer)

# # Combine the existing and new consumers
# consumers.extend(new_consumers)

# # Save the updated list to a new JSON file
# with open(output_file_path, 'w', encoding='utf-8') as file:
#     json.dump(consumers, file, indent=4, ensure_ascii=False)

# output_file_path

