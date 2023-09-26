h = 0
while h < 1 or h > 8:
    try:
        h = int(input("Height: "))
    except ValueError:
        print("Please enter a valid integer.")

for i in range(h):
    print(" " * (h - i - 1), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1), end="")
    print()