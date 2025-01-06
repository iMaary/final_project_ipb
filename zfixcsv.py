# Tentativa de corrigir strings com aspas abertas
with open('result1000p1000c.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Escrevendo um novo arquivo corrigido
with open('result1000p1000c_fixed.csv', 'w', encoding='utf-8') as file:
    for line in lines:
        # Remove quebras inesperadas de linha
        line = line.replace('\n', '').replace('\r', '')
        file.write(line + '\n')
