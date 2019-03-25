def to_base_3(number, c):
	acc = []
	while number > 0:
		acc += [number % 3]
		number //= 3
	return acc

print(to_base_3(10, 4))
