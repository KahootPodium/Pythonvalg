import string, random

symbols = string.printable[:62]
keys = []

shift = 4
length = 4

for key in range(10):
    seed = "".join(random.choice(symbols) for symbol in range(length))
    group = symbols.index(seed[-1]) + shift

    keys.append(seed + symbols[group % (len(symbols) - 1)])
    
print(keys)
