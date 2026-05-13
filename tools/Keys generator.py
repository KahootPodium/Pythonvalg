import string, random

symbols = string.printable[:63]
keys = []

names = ["IMSTIT", "IMSTMP", "IMIT", "IMMP"]
quantity = [20, 11, 17, 16]

length = 4

for quantity, name in zip(quantity, names):
    shift = names.index(name) + 1

    for key in range(quantity):
        seed = "".join(random.choice(symbols) for symbol in range(length))
        group = symbols.index(seed[-1]) + shift * 1

        keys.append(name + ":" + seed + symbols[group % (len(symbols) - 1)])
        
    keys.append("")

open("Keys.txt", "w").writelines(key + "\n" for key in keys)