import string

symbols = string.printable[:63]
key = "8prab"

print((symbols.index(key[-1]) - symbols.index(key[-2])) % (len(symbols) - 1))
