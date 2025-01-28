from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height <= 8 and height > 0:
        break

for i in range(1, height + 1):
    n = height - i
    print(" " * n, end="")
    print("#" * i, end="  ")
    print("#" * i, end="")
    print()
